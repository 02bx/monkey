import httplib

import flask_restful
from flask import jsonify

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.reporting.report import ReportService

ZERO_TRUST_REPORT_TYPE = "zero_trust"
GENERAL_REPORT_TYPE = "general"
REPORT_TYPES = [GENERAL_REPORT_TYPE, ZERO_TRUST_REPORT_TYPE]

__author__ = ["itay.mizeretz", "shay.nehmad"]


class Report(flask_restful.Resource):

    @jwt_required()
    def get(self, report_type):
        if report_type == GENERAL_REPORT_TYPE:
            return ReportService.get_report()
        elif report_type == ZERO_TRUST_REPORT_TYPE:
            fakedict = {
                "are_all_monkeys_done": False,
                "findings": [
                    {
                        "test": "Monkey 8 found a machine with no AV software active.",
                        "conclusive": False,
                        "pillars": ["Devices"],
                        "events": [
                            {
                                "timestamp": "2019-08-01 14:48:46.112000",
                                "title": "Monkey perform an action",
                                "message": "log1"
                            }, {
                                "timestamp": "2019-08-01 14:48:42.112000",
                                "title": "Analysis",
                                "message": "log2"
                            }]
                    },
                    {
                        "test": "Monkey 6 successfully exploited machine XXX with shellshock.",
                        "conclusive": True,
                        "pillars": ["Devices", "Networks"],
                        "events": [
                            {
                                "timestamp": "2019-08-01 14:48:46.112000",
                                "title": "Analysis",
                                "message": "log3"
                            }]
                    }
                ]
            }
            return jsonify(fakedict)

        flask_restful.abort(httplib.NOT_FOUND)
