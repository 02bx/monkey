import json
import re
import urllib2

__author__ = 'itay.mizeretz'

AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS = "169.254.169.254"
AWS_LATEST_METADATA_URI_PREFIX = 'http://{0}/latest/'.format(AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS)
ACCOUNT_ID_KEY = "accountId"


class AwsInstance(object):
    """
    Class which gives useful information about the current instance you're on.
    """

    def __init__(self):
        try:
            self.instance_id = urllib2.urlopen(
                AWS_LATEST_METADATA_URI_PREFIX + 'meta-data/instance-id', timeout=2).read()
            self.region = self._parse_region(
                urllib2.urlopen(AWS_LATEST_METADATA_URI_PREFIX + 'meta-data/placement/availability-zone').read())
        except urllib2.URLError:
            self.instance_id = None
            self.region = None
        try:
            self.account_id = self._extract_account_id(
                urllib2.urlopen(
                    AWS_LATEST_METADATA_URI_PREFIX + 'dynamic/instance-identity/document', timeout=2).read())
        except urllib2.URLError:
            self.account_id = None

    @staticmethod
    def _parse_region(region_url_response):
        # For a list of regions, see:
        # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
        # This regex will find any AWS region format string in the response.
        re_phrase = r'((?:us|eu|ap|ca|cn|sa)-[a-z]*-[0-9])'
        finding = re.findall(re_phrase, region_url_response, re.IGNORECASE)
        if finding:
            return finding[0]
        else:
            return None

    def get_instance_id(self):
        return self.instance_id

    def get_region(self):
        return self.region

    def is_aws_instance(self):
        return self.instance_id is not None

    @staticmethod
    def _extract_account_id(instance_identity_document_response):
        return json.loads(instance_identity_document_response)[ACCOUNT_ID_KEY]

    def get_account_id(self):
        return self.account_id
