from cc.database import mongo
from cc.services.node import NodeService

__author__ = "itay.mizeretz"


class ReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_first_monkey_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', 1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_last_monkey_dead_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', -1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_breach_count():
        return mongo.db.edge.count({'exploits.result': True})

    @staticmethod
    def get_successful_exploit_types():
        exploit_types = mongo.db.command({'distinct': 'edge', 'key': 'exploits.exploiter'})['values']
        return [exploit for exploit in exploit_types if ReportService.did_exploit_type_succeed(exploit)]

    @staticmethod
    def get_tunnels():
        return [
            (NodeService.get_monkey_label_by_id(tunnel['_id']), NodeService.get_monkey_label_by_id(tunnel['tunnel']))
            for tunnel in mongo.db.monkey.find({'tunnel': {'$exists': True}}, {'tunnel': 1})]

    @staticmethod
    def get_scanned():
        nodes =\
            [NodeService.get_displayed_node_by_id(node['_id']) for node in mongo.db.node.find({}, {'_id': 1})]\
            + [NodeService.get_displayed_node_by_id(monkey['_id']) for monkey in mongo.db.monkey.find({}, {'_id': 1})]
        nodes = [
            {
                'label': node['label'],
                'ip_addresses': node['ip_addresses'],
                'accessible_from_nodes': node['accessible_from_nodes'],
                'services': node['services']
            }
            for node in nodes]

        return nodes

    @staticmethod
    def get_exploited():
        exploited =\
            [NodeService.get_displayed_node_by_id(monkey['_id']) for monkey in mongo.db.monkey.find({}, {'_id': 1})
             if not NodeService.get_monkey_manual_run(NodeService.get_monkey_by_id(monkey['_id']))]\
            + [NodeService.get_displayed_node_by_id(node['_id'])
               for node in mongo.db.node.find({'exploited': True}, {'_id': 1})]

        exploited = [
            {
                'label': monkey['label'],
                'ip_addresses': monkey['ip_addresses'],
                'exploits': [exploit['exploiter'] for exploit in monkey['exploits'] if exploit['result']]
            }
            for monkey in exploited]

        return exploited

    @staticmethod
    def get_report():
        return \
            {
                'first_monkey_time': ReportService.get_first_monkey_time(),
                'last_monkey_dead_time': ReportService.get_last_monkey_dead_time(),
                'breach_count': ReportService.get_breach_count(),
                'successful_exploit_types': ReportService.get_successful_exploit_types(),
                'tunnels': ReportService.get_tunnels(),
                'scanned': ReportService.get_scanned(),
                'exploited': ReportService.get_exploited()
            }

    @staticmethod
    def did_exploit_type_succeed(exploit_type):
        return mongo.db.edge.count(
            {'exploits': {'$elemMatch': {'exploiter': exploit_type, 'result': True}}},
            limit=1) > 0
