import logging
from infection_monkey.utils.load_plugins import get_instances
from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


def get_fingerprint_instances():
    """
    Returns the fingerprint objects according to configuration as a list
    :return: A list of HostFinger objects.
    """
    return get_instances(__package__, __file__, HostFinger)
