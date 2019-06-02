from infection_monkey.telemetry.attack.attack_telem import AttackTelem

__author__ = "VakarisZ"


class VictimHostTelem(AttackTelem):

    def __init__(self, technique, status, machine):
        """
        ATT&CK telemetry that parses and sends VictimHost's (remote machine's) data
        :param technique: Technique ID. E.g. T111
        :param status: ScanStatus of technique
        :param machine: VictimHost obj from model/host.py
        """
        super(VictimHostTelem, self).__init__(technique, status)
        self.machine = {'domain_name': machine.domain_name, 'ip_addr': machine.ip_addr}

    def get_data(self):
        return super(VictimHostTelem, self).get_data().update({
            'machine': self.machine
        })
