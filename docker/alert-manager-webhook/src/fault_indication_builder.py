# --------------------------------------------------------------------------
#  COPYRIGHT Ericsson 2022
#
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.
# --------------------------------------------------------------------------
import datetime
from functools import reduce
import helper
from custom_field_parser import *

DEFAULT_VALUE = 'UNKNOWN'
REQUIRED_FIELDS = ["faultName", "serviceName", "createdAt"]
CUSTOM_FIELD_PARSER_KEY = "CustomFieldParser:"

class FaultIndicationBuilder:

    def __init__(self, mapping):
        self.logger = helper.get_logger()
        self.mapping = mapping

    def build(self, alert):
        """
        Set the mandatory parameters required to raise/clear Fault Indication
        and return the fm alarm data in json format
        """

        self.logger.debug("Alert details from notification received :{}".format(alert))
        fault_indication = {}

        """
        check if the mapping.yaml key is in a dict or list
        remember that mapping[key] = value of the key so this is usually a list 
        so he checks if the mapping[key] is a list and that the length of list (there is 1 dict in mapping.yaml
        for additional information
        """

        if self.mapping:
            for key in self.mapping:
                if isinstance(self.mapping[key], list) and len(self.mapping[key]) > 0:
                    value = self.get_mapped_value(alert, self.mapping[key])
                    formatted_value = self.format_value(alert, key, value)
                    if formatted_value is not None:
                        fault_indication[key] = formatted_value

                elif isinstance(self.mapping[key], dict):
                    fault_indication[key] = {}
                    for nested_key in self.mapping[key]:
                        if isinstance(self.mapping[key][nested_key], list):
                            value = self.get_mapped_value(alert, self.mapping[key][nested_key])
                            if value is not None:
                                fault_indication[key][nested_key] = value
                        else:
                            self.logger.error("Invalid configuration for key: [{}, {}], value: {}"
                                              .format(key, nested_key, self.mapping[key][nested_key]))

                else:
                    self.logger.error("Invalid configuration for key: {}, value: {}".format(key, self.mapping[key]))

        for required_key in REQUIRED_FIELDS:
            if required_key not in fault_indication.keys() or not fault_indication[required_key]:
                self.fill_required(fault_indication, required_key)

        self.logger.info("Fault Indication Built from Alarm :{}".format(fault_indication))
        return fault_indication

    """
        the mapping_keys are the values on the key in mapping.yaml 
        if more than 1 mapping key is provided the loop will exit once it finds  match
        say the mapping keys are [['labels','deployment'],  ['labels','statefulset'],  ['labels','daemonset']]
        itf it finds say labels:statefulset then it exits and returns the value of this            
    """

    def get_mapped_value(self, alert, mapping_keys):
        if isinstance(mapping_keys, list):
            for key in mapping_keys:
                if isinstance(key, str) and key.startswith(CUSTOM_FIELD_PARSER_KEY):
                    return self.get_custom_parser_value(key, alert)
                if isinstance(key, list):
                    value = reduce(dict.get, key, alert)
                    if value:
                        return value

    def format_value(self, alert, key, value):
        if key == 'expiration':
            return self.get_expiration(alert, value)
        elif key == 'severity':
            if alert['status'] == 'resolved':
                return 'Clear'
            return value.capitalize()
        return value

    def get_expiration(self, alert, ends_at):
        starts_at = None
        if 'createdAt' in self.mapping.keys():
            starts_at = self.get_mapped_value(alert, self.mapping['createdAt'])
        if not starts_at and 'startsAt' in alert.keys():
            starts_at = alert['startsAt']
        if not starts_at or not ends_at:
            return 0
        try:
            created_at_obj = helper.convert_str_to_date(starts_at)
            ends_at_obj = helper.convert_str_to_date(ends_at)
            if ends_at_obj > created_at_obj:
                return int((ends_at_obj - created_at_obj).total_seconds())
        except:
            self.logger.error('Error converting string to date [start: {}, end: {}]'.format(starts_at, ends_at))
        return 0

    def fill_required(self, fault_indication, key):
        if key == 'createdAt':
            fault_indication[key] = datetime.datetime.now().isoformat()+'Z'
        else:
            fault_indication[key] = DEFAULT_VALUE

    def get_custom_parser_value(self, key, alert):
        parser_name = key.replace(CUSTOM_FIELD_PARSER_KEY, '')
        parser_obj = eval(parser_name + "()")
        if isinstance(parser_obj, CustomFieldParserInterface):
            return parser_obj.parse_field(alert, self.mapping)