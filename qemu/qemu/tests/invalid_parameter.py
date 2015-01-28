import logging
from autotest.client.shared import error
from virttest import env_process
from virttest import virt_vm


@error.context_aware
def run(test, params, env):
    """
    Qemu invalid parameter in qemu command line test:
    1) Try boot up guest with invalid parameters
    2) Catch the error message shows by qemu process

    :param test: QEMU test object
    :param params: Dictionary with the test parameters
    :param env: Dictionary with test environment.
    """
    vm_name = params["main_vm"]
    params['start_vm'] = "yes"
    try:
        error.context("Start guest with invalid parameters.")
        env_process.preprocess_vm(test, params, env, vm_name)
        vm = env.get_vm(vm_name)
        vm.destroy()
        raise error.TestFail("Guest start normally, didn't quit as expect.")
    except Exception, emsg:
        error.context("Check guest exit status.")
        if "(core dumped)" in emsg.reason:
            raise error.TestFail("Guest core dumped with invalid parameters.")
        else:
            logging.info("Guest quit as expect: %s" % emsg.reason)
