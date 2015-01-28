import time
import logging
import re
from autotest.client.shared import error
from autotest.client.shared import utils
from virttest import utils_test
from virttest import utils_misc
from virttest import env_process
from virttest import utils_net


@error.context_aware
def run(test, params, env):
    """
    Qemu host nic bonding test:
    1) Load bonding module with mode 802.3ad
    2) Bring up bond interface
    3) Add nics to bond interface
    4) Add a new bridge and add bond interface to it
    5) Get ip address for bridge
    6) Boot up guest with the bridge
    7) Checking guest netowrk via ping
    8) Start file transfer between guest and host
    9) Disable and enable physical interfaces during file transfer

    :param test: QEMU test object
    :param params: Dictionary with the test parameters
    :param env: Dictionary with test environment.
    """
    bond_iface = params.get("bond_iface", "bond0")
    bond_br_name = params.get("bond_br_name", "br_bond0")
    timeout = int(params.get("login_timeout", 240))
    remote_host = params.get("dsthost")
    ping_timeout = int(params.get("ping_timeout", 240))
    bonding_timeout = int(params.get("bonding_timeout", 1))
    params['netdst'] = bond_br_name

    error.context("Load bonding module with mode 802.3ad", logging.info)
    if not utils.system("lsmod|grep bonding", ignore_status=True):
        utils.system("modprobe -r bonding")

    utils.system("modprobe bonding mode=802.3ad")

    error.context("Bring up %s" % bond_iface, logging.info)
    host_ifaces = utils_net.get_host_iface()

    if bond_iface not in host_ifaces:
        raise error.TestError("Can not find bond0 in host")

    bond_iface = utils_net.Interface(bond_iface)
    bond_iface.up()
    bond_mac = bond_iface.get_mac()

    host_ph_iface_pre = params.get("host_ph_iface_prefix", "en")
    host_iface_bonding = int(params.get("host_iface_bonding", 2))

    host_ph_ifaces = [_ for _ in host_ifaces if re.match(host_ph_iface_pre, _)]

    if len(host_ph_ifaces) < 2 or len(host_ph_ifaces) < host_iface_bonding:
        raise error.TestErrorNA("Host need %s nics"
                                " at least." % host_iface_bonding)

    error.context("Add nics to %s" % bond_iface.name, logging.info)
    host_ifaces_bonding = host_ph_ifaces[:host_iface_bonding]
    ifenslave_cmd = "ifenslave %s" % bond_iface.name
    op_ifaces = []
    for host_iface_bonding in host_ifaces_bonding:
        op_ifaces.append(utils_net.Interface(host_iface_bonding))
        ifenslave_cmd += " %s" % host_iface_bonding
    utils.system(ifenslave_cmd)

    error.context("Add a new bridge and add %s to it." % bond_iface.name,
                  logging.info)
    bonding_bridge = utils_net.Bridge()
    if bond_br_name not in bonding_bridge.list_br():
        bonding_bridge.add_bridge(bond_br_name)
    bonding_bridge.add_port(bond_br_name, bond_iface.name)

    error.context("Get ip address for bridge", logging.info)
    utils.system("pkill dhclient; dhclient %s" % bond_br_name)

    error.context("Boot up guest with bridge %s" % bond_br_name, logging.info)
    params["start_vm"] = "yes"
    vm_name = params.get("main_vm")
    env_process.preprocess_vm(test, params, env, vm_name)
    vm = env.get_vm(vm_name)
    session = vm.wait_for_login(timeout=timeout)

    error.context("Checking guest netowrk via ping.", logging.info)
    ping_cmd = params.get("ping_cmd")
    ping_cmd = re.sub("REMOTE_HOST", remote_host, ping_cmd)
    session.cmd(ping_cmd, timeout=ping_timeout)

    error.context("Start file transfer", logging.info)
    f_transfer = utils.InterruptedThread(utils_test.run_virt_sub_test,
                                         args=(test, params, env,),
                                         kwargs={"sub_type": "file_transfer"})
    f_transfer.start()
    utils_misc.wait_for(lambda: utils.system_output("pidof scp",
                                                    ignore_status=True), 30)

    error.context("Disable and enable physical "
                  "interfaces in %s" % bond_br_name, logging.info)
    while True:
        for op_iface in op_ifaces:
            logging.debug("Turn down %s" % op_iface.name)
            op_iface.down()
            time.sleep(bonding_timeout)
            logging.debug("Bring up %s" % op_iface.name)
            op_iface.up()
            time.sleep(bonding_timeout)
        if not f_transfer.is_alive():
            break
    f_transfer.join()
