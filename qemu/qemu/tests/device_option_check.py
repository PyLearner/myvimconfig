import logging
import re
from autotest.client.shared import error
from virttest import utils_misc
from virttest import env_process
from virttest import qemu_qtree


@error.context_aware
def run(test, params, env):
    """
    Qemu device options value check test:

    1) Boot up guest with setted option value
    2) Check the value is correct inside guest

    :param test: QEMU test object
    :param params: Dictionary with the test parameters
    :param env: Dictionary with test environment.
    """
    error.context("Boot up guest.", logging.info)
    timeout = float(params.get("login_timeout", 240))
    vm = env.get_vm(params["main_vm"])
    parameter_value = params.get("parameter_value", "random")
    params_name = params["params_name"]
    parameter_prefix = params.get("parameter_prefix", "")
    check_cmds = params["check_cmds"]
    convert_str = params.get("convert_str")

    if params.get("start_vm") == "no":
        if parameter_value == "random":
            parameter_len = int(params.get("parameter_len", 4))
            random_ignore_str = params.get("ignore_str")
            func_generate_random_string = utils_misc.generate_random_string
            args = (parameter_len, )
            if random_ignore_str:
                args += ("ignore_str=%s" % random_ignore_str, )
            if convert_str:
                args += ("convert_str=%s" % convert_str, )
            parameter_value = func_generate_random_string(*args)

        params[params_name] = parameter_prefix + parameter_value
        logging.debug("Setup '%s' to '%s'" % (params_name,
                                              params[params_name]))

        params["start_vm"] = "yes"
        env_process.preprocess_vm(test, params, env, vm.name)

    if convert_str:
        tmp_str = re.sub(r'\\\\', 'Abackslash', parameter_value)
        tmp_str = re.sub(r'\\', '', tmp_str)
        tmp_str = re.sub('Abackslash', r"\\", tmp_str)
        parameter_value_raw = tmp_str
    else:
        parameter_value_raw = parameter_value

    if params.get("check_in_qtree") == "yes":
        error.context("Check option in qtree", logging.info)
        qtree = qemu_qtree.QtreeContainer()
        try:
            qtree.parse_info_qtree(vm.monitor.info('qtree'))
        except AttributeError:
            logging.debug("Monitor deson't support info qtree skip this test")
            qtree = None
        if qtree:
            keyword = params['qtree_check_keyword']
            qtree_check_value = params['qtree_check_value']
            qtree_check_option = params['qtree_check_option']
            for qdev in qtree.get_nodes():
                if (keyword in qdev.qtree
                        and qdev.qtree[keyword] == qtree_check_value):
                    qtree_value = qdev.qtree.get(qtree_check_option)
                    if re.match('".*"$', qtree_value):
                        qtree_value = re.findall('"(.*)"$', qtree_value)[0]
                    if qtree_value != parameter_value_raw:
                        raise error.TestFail("Value from info qtree is not "
                                             "match with the value from "
                                             "command line: %s vs "
                                             "%s" % (qtree_value,
                                                     parameter_value_raw))

    session = vm.wait_for_login(timeout=timeout)

    failed_log = ""
    for check_cmd in check_cmds.split():
        check_cmd_params = params.object_params(check_cmd)
        cmd = check_cmd_params['cmd']
        pattern = check_cmd_params['pattern'] % parameter_value_raw

        error.context("Check option with command %s" % cmd, logging.info)
        _, output = session.cmd_status_output(cmd)
        if not re.findall(r'%s' % pattern, output):
            failed_log += ("Can not find option %s from guest."
                           " Guest output is '%s'" % (params_name,
                                                      output))

    session.close()

    if failed_log:
        raise error.TestFail(failed_log)
