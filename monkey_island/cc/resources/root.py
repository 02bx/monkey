from datetime import datetime

from flask import request, make_response, jsonify
import flask_restful

from cc.database import mongo

from cc.utils import local_ip_addresses

__author__ = 'Barak'


class Root(flask_restful.Resource):
    def get(self, action=None):
        if not action:
            action = request.args.get('action')

        if not action:
            return jsonify(ip_addresses=local_ip_addresses(), mongo=str(mongo.db), completed_steps=self.get_completed_steps())

        elif action == "reset":
            mongo.db.config.drop()
            mongo.db.monkey.drop()
            mongo.db.telemetry.drop()
            mongo.db.node.drop()
            mongo.db.edge.drop()
            return jsonify(status='OK')
        elif action == "killall":
            mongo.db.monkey.update({}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}}, upsert=False,
                                   multi=True)
            return 200
        else:
            return make_response(400, {'error': 'unknown action'})

    def get_completed_steps(self):
        # TODO implement
        return dict(run_server=True, run_monkey=False, infection_done=False)
