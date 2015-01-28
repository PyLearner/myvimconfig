import logging
from autotest.client.shared import error
from autotest.client import utils
from virttest import base_installer, utils_misc


def run(test, params, env):
    """
    load/unload kernel modules several times.

    This tests the kernel pre-installed kernel modules
    """
    installer_object = base_installer.NoopInstaller('noop',
                                                    'module_probe',
                                                    test, params)
    logging.debug('installer object: %r', installer_object)
    submodules = []
    modules_str = " "
    for module in installer_object.module_list:
        if " %s " % module in modules_str:
            continue
        tmp_list = [module]
        if utils.module_is_loaded(module):
            tmp_list += utils.get_submodules(module)
        modules_str += "%s " % " ".join(tmp_list)
        if len(tmp_list) > 1:
            for _ in submodules:
                if _[0] in tmp_list:
                    submodules.remove(_)
                    break
        submodules.append(tmp_list)

    installer_object.module_list = []
    for submodule_list in submodules:
        installer_object.module_list += submodule_list

    load_count = int(params.get("load_count", 100))
    try:
        # unload the modules before starting:
        installer_object.unload_modules()
        for _ in range(load_count):
            try:
                installer_object.load_modules()
            except base_installer.NoModuleError, e:
                logging.error(e)
                break
            except Exception, e:
                raise error.TestFail("Failed to load modules [%r]: %s" %
                                     (installer_object.module_list, e))
            installer_object.unload_modules()
    finally:
        try:
            installer_object.load_modules()
        except base_installer.NoModuleError:
            pass
