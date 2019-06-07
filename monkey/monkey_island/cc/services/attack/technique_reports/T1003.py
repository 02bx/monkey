from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1003(AttackTechnique):

    tech_id = "T1003"
    unscanned_msg = "Monkey tried to obtain credentials from systems in the network but didn't find any or failed."
    scanned_msg = "Monkey tried to obtain credentials from systems in the network but didn't find any or failed."
    used_msg = "Monkey successfully obtained some credentials from systems on the network."

    query = {'telem_type': 'system_info_collection', '$and': [{'data.credentials': {'$exists': True}},
                                                              {'data.credentials': {'$gt': {}}}]}

    @staticmethod
    def get_report_data():
        data = {'title': T1003.technique_title(T1003.tech_id)}
        if mongo.db.telemetry.count_documents(T1003.query):
            data.update({'message': T1003.used_msg, 'status': ScanStatus.USED.name})
        else:
            data.update({'message': T1003.unscanned_msg, 'status': ScanStatus.UNSCANNED.name})
        return data
