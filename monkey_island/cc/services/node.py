import datetime
from bson import ObjectId

from cc.database import mongo
from cc.services.edge import EdgeService
from cc.utils import local_ip_addresses
__author__ = "itay.mizeretz"


class NodeService:
    def __init__(self):
        pass

    @staticmethod
    def get_displayed_node_by_id(node_id):
        if ObjectId(node_id) == ObjectId("000000000000000000000000"):
            return NodeService.get_monkey_island_node()

        edges = EdgeService.get_displayed_edges_by_to(node_id)
        accessible_from_nodes = []
        exploits = []

        new_node = {"id": node_id}

        node = NodeService.get_node_by_id(node_id)
        if node is None:
            monkey = NodeService.get_monkey_by_id(node_id)
            if monkey is None:
                return new_node

            # node is infected
            new_node = NodeService.monkey_to_net_node(monkey)
            for key in monkey:
                # TODO: do something with tunnel
                if key not in ["_id", "modifytime", "parent", "tunnel", "dead"]:
                    new_node[key] = monkey[key]

        else:
            # node is uninfected
            new_node = NodeService.node_to_net_node(node)
            new_node["ip_addresses"] = node["ip_addresses"]

        for edge in edges:
            accessible_from_nodes.append({"id": edge["from"]})
            for exploit in edge["exploits"]:
                exploit["origin"] = NodeService.get_monkey_label(NodeService.get_monkey_by_id(edge["from"]))
                exploits.append(exploit)

        exploits.sort(cmp=NodeService._cmp_exploits_by_timestamp)

        new_node["exploits"] = exploits
        new_node["accessible_from_nodes"] = accessible_from_nodes
        if len(edges) > 0:
            new_node["services"] = edges[-1]["services"]

        # TODO: add exploited by

        return new_node

    @staticmethod
    def get_node_label(node):
        return node["os"]["version"] + " : " + node["ip_addresses"][0]

    @staticmethod
    def _cmp_exploits_by_timestamp(exploit_1, exploit_2):
        if exploit_1["start_timestamp"] == exploit_2["start_timestamp"]:
            return 0
        if exploit_1["start_timestamp"] > exploit_2["start_timestamp"]:
            return 1
        return -1

    @staticmethod
    def get_monkey_os(monkey):
        os = "unknown"
        if monkey["description"].lower().find("linux") != -1:
            os = "linux"
        elif monkey["description"].lower().find("windows") != -1:
            os = "windows"
        return os

    @staticmethod
    def get_monkey_manual_run(monkey):
        for p in monkey["parent"]:
            if p[0] != monkey["guid"]:
                return False

        return True


    @staticmethod
    def get_monkey_label(monkey):
        return monkey["hostname"] + " : " + monkey["ip_addresses"][0]

    @staticmethod
    def get_monkey_group(monkey):
        if len(set(monkey["ip_addresses"]).intersection(local_ip_addresses())) != 0:
            return "islandInfected"

        return "manuallyInfected" if NodeService.get_monkey_manual_run(monkey) else "infected"

    @staticmethod
    def monkey_to_net_node(monkey):
        return \
            {
                "id": monkey["_id"],
                "label": NodeService.get_monkey_label(monkey),
                "group": NodeService.get_monkey_group(monkey),
                "os": NodeService.get_monkey_os(monkey),
                "dead": monkey["dead"],
            }

    @staticmethod
    def node_to_net_node(node):
        return \
            {
                "id": node["_id"],
                "label": NodeService.get_node_label(node),
                "group": "clean",
                "os": node["os"]["type"]
            }

    @staticmethod
    def unset_all_monkey_tunnels(monkey_id):
        mongo.db.edge.update(
            {"from": monkey_id, 'tunnel': True},
            {'$set': {'tunnel': False}},
            upsert=False)

    @staticmethod
    def set_monkey_tunnel(monkey_id, tunnel_host_id):
        tunnel_edge = EdgeService.get_or_create_edge(monkey_id, tunnel_host_id)
        mongo.db.edge.update({"_id": tunnel_edge["_id"]},
                             {'$set': {'tunnel': True}},
                             upsert=False)

    @staticmethod
    def insert_node(ip_address):
        new_node_insert_result = mongo.db.node.insert_one(
            {
                "ip_addresses": [ip_address],
                "os":
                    {
                        "type": "unknown",
                        "version": "unknown"
                    }
            })
        return mongo.db.node.find_one({"_id": new_node_insert_result.inserted_id})

    @staticmethod
    def get_or_create_node(ip_address):
        new_node = mongo.db.node.find_one({"ip_addresses": ip_address})
        if new_node is None:
            new_node = NodeService.insert_node(ip_address)
        return new_node

    @staticmethod
    def get_monkey_by_id(monkey_id):
        return mongo.db.monkey.find_one({"_id": ObjectId(monkey_id)})

    @staticmethod
    def get_monkey_by_guid(monkey_guid):
        return mongo.db.monkey.find_one({"guid": monkey_guid})

    @staticmethod
    def get_monkey_by_ip(ip_address):
        return mongo.db.monkey.find_one({"ip_addresses": ip_address})

    @staticmethod
    def get_node_by_ip(ip_address):
        return mongo.db.node.find_one({"ip_addresses": ip_address})

    @staticmethod
    def get_node_by_id(node_id):
        return mongo.db.node.find_one({"_id": ObjectId(node_id)})

    @staticmethod
    def update_monkey_modify_time(monkey_id):
        mongo.db.monkey.update({"_id": monkey_id},
                               {"$set": {"modifytime": datetime.now()}},
                               upsert=False)

    @staticmethod
    def set_monkey_dead(monkey, is_dead):
        mongo.db.monkey.update({"guid": monkey['guid']},
                               {'$set': {'dead': is_dead}},
                               upsert=False)

    @staticmethod
    def get_monkey_island_monkey():
        ip_addresses = local_ip_addresses()
        for ip_address in ip_addresses:
            monkey = NodeService.get_monkey_by_ip(ip_address)
            if monkey is not None:
                return monkey
        return None

    @staticmethod
    def get_monkey_island_pseudo_net_node():
        return\
            {
                "id": ObjectId("000000000000000000000000"),
                "label": "MonkeyIsland",
                "group": "islandClean",
            }

    @staticmethod
    def get_monkey_island_node():
        island_node = NodeService.get_monkey_island_pseudo_net_node()
        island_node["ip_addresses"] = local_ip_addresses()
        return island_node
