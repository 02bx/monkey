from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting.report import ReportService
from common.utils.attack_utils import ScanStatus
from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES


__author__ = "shreyamalviya"


class T1158(AttackTechnique):
    tech_id = "T1158"
    unscanned_msg = "Monkey did not try creating hidden files or folders."
    scanned_msg = "Monkey tried creating hidden files and folders on the system but failed."
    used_msg = "Monkey created hidden files and folders on the system."

    @staticmethod
    def get_report_data():
        data = {'title': T1158.technique_title(), 'info': []}

        scanned_nodes = ReportService.get_scanned()
        status = ScanStatus.UNSCANNED.value

        for node in scanned_nodes:
            if node['pba_results'] != 'None':
                for pba in node['pba_results']:
                    if pba['name'] == POST_BREACH_HIDDEN_FILES:
                        status = ScanStatus.USED.value if pba['result'][1]\
                                                       else ScanStatus.SCANNED.value
                        data['info'].append({
                                'machine': {
                                    'hostname': pba['hostname'],
                                    'ips': node['ip_addresses']
                                },
                                'type': 'Folder' if 'folder' in pba['command'] else 'File',
                                'result': pba['result'][0]
                            })
            data.update(T1158.get_base_data_by_status(status))
        return data
