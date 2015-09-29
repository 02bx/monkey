import os
import sys
import subprocess
import logging
from network import HostScanner, HostFinger
from model.host import VictimHost
import re

__author__ = 'itamar'

PING_COUNT_FLAG = "-n" if "win32" == sys.platform else "-c"
PING_TIMEOUT_FLAG = "-w" if "win32" == sys.platform else "-W"
TTL_REGEX_STR = '(?<=TTL\=)[0-9]+'
LINUX_TTL = 64
WINDOWS_TTL = 128

LOG = logging.getLogger(__name__)

class PingScanner(HostScanner, HostFinger):
    def __init__(self):
        self._config = __import__('config').WormConfiguration
        self._devnull = open(os.devnull, "w")
        self._ttl_regex = re.compile(TTL_REGEX_STR, re.IGNORECASE)

    def is_host_alive(self, host):
        assert isinstance(host, VictimHost)

        timeout = self._config.ping_scan_timeout
        if not "win32" == sys.platform:
            timeout = timeout / 1000

        return 0 == subprocess.call(["ping",
                                     PING_COUNT_FLAG, "1",
                                     PING_TIMEOUT_FLAG, str(timeout),
                                     host.ip_addr],
                                    stdout=self._devnull,
                                    stderr=self._devnull)

    def get_host_fingerprint(self, host):
        assert isinstance(host, VictimHost)

        timeout = self._config.ping_scan_timeout
        if not "win32" == sys.platform:
            timeout = timeout / 1000

        sub_proc = subprocess.Popen(["ping", 
                        PING_COUNT_FLAG,
                        "1", 
                        PING_TIMEOUT_FLAG, 
                        str(timeout), host.ip_addr], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)

        output = " ".join(sub_proc.communicate())
        regex_result = self._ttl_regex.search(output)
        if regex_result:
            try:
                ttl = int(regex_result.group(0))
                if LINUX_TTL == ttl:
                    host.os['type'] = 'linux'
                elif WINDOWS_TTL == ttl:
                    host.os['type'] = 'windows'
                return True
            except Exception, exc:
                LOG.debug("Error parsing ping fingerprint: %s", exc)

        return False
