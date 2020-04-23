import logging
from datetime import timedelta
import json

from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.tests.performance.utils.telem_parser import TelemParser
from envs.monkey_zoo.blackbox.analyzers.performance_analyzer import PerformanceAnalyzer
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import PerformanceTestConfig
from envs.monkey_zoo.blackbox.island_client.supported_reuqest_method import SupportedRequestMethod

LOGGER = logging.getLogger(__name__)

MAX_ALLOWED_SINGLE_TELEM_PARSE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=60)


class TelemetryPerformanceTest:

    def __init__(self, island_client: MonkeyIslandClient):
        self.island_client = island_client

    def test_telemetry_performance(self):
        LOGGER.info("Starting telemetry performance test.")
        try:
            all_telemetries = TelemParser.get_all_telemetries()
        except FileNotFoundError:
            LOGGER.error("Telemetries to send not found. Refer to readme to figure out how to generate telemetries "
                         "and where to put them.")
            return False
        LOGGER.info("Telemetries imported successfully.")
        all_telemetries.sort(key=lambda telem: telem['time']['$date'])
        telemetry_parse_times = {}
        for telemetry in all_telemetries:
            telemetry_endpoint = TelemetryPerformanceTest.get_verbose_telemetry_endpoint(telemetry)
            telemetry_parse_times[telemetry_endpoint] = self.get_telemetry_time(telemetry)
        test_config = PerformanceTestConfig(MAX_ALLOWED_SINGLE_TELEM_PARSE_TIME, MAX_ALLOWED_TOTAL_TIME)
        PerformanceAnalyzer(test_config, telemetry_parse_times).analyze_test_results()

    def get_telemetry_time(self, telemetry):
        content = telemetry['content']
        url = telemetry['endpoint']
        method = SupportedRequestMethod.__getattr__(telemetry['method'])

        return self.island_client.requests.get_request_time(url=url, method=method, data=content)

    @staticmethod
    def get_verbose_telemetry_endpoint(telemetry):
        telem_category = ""
        if "telem_category" in telemetry['content']:
            telem_category = "_" + json.loads(telemetry['content'])['telem_category']
        return telemetry['endpoint'] + telem_category
