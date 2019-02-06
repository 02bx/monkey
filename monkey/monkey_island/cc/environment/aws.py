import cc.auth
from cc.environment import Environment
from common.cloud.aws import AWS
from Crypto.Hash import SHA3_512
__author__ = 'itay.mizeretz'


class AwsEnvironment(Environment):
    def __init__(self):
        super(AwsEnvironment, self).__init__()
        self.aws_info = AWS()
        self._instance_id = self._get_instance_id()
        self.region = self._get_region()

    def _get_instance_id(self):
        return self.aws_info.get_instance_id()

    def _get_region(self):
        return self.aws_info.get_region()

    def is_auth_enabled(self):
        return True

    def get_auth_users(self):
        return [
            cc.auth.User(1, 'monkey', self.hash_secret(self._instance_id))
        ]
