# --------------------------------------------------------------------------
#  COPYRIGHT Ericsson 2022
#
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.
# --------------------------------------------------------------------------
import os
import helper

RES_FOLDER = os.path.join(os.path.dirname(__file__), "resources") + os.path.sep


class CustomFieldParserInterface:
    def parse_field(self, alert: dict, mapping: dict) -> str:
        """ Receives a dict containing the alert e returns the value of a field parsed with a custom logic. """
        pass


class FaultNameParser(CustomFieldParserInterface):

    prefixes_to_remove = ['eric-eo-cm-', 'eric-eo-', 'eric-']

    def parse_field(self, alert: dict, mapping: dict) -> str:
        service_name = helper.get_mapped_value(alert, mapping['serviceName'])
        max_length = 64 - len(service_name)
        service_name = self.remove_prefixes(service_name)
        service_name_formatted = ''
        for word in service_name.split('-'):
            service_name_formatted += word[:3].capitalize()
        alert_name = ''
        if 'labels' in alert and 'alertname' in alert['labels']:
            alert_name = alert['labels']['alertname']
        alert_name = self.get_short_alert_name(alert_name)
        return (alert_name + service_name_formatted)[:max_length]

    def remove_prefixes(self, service_name):
        for prefix in self.prefixes_to_remove:
            service_name = service_name.replace(prefix, '')
        return service_name

    def get_short_alert_name(self, alert_name):
        short_names = helper.load_yaml(RES_FOLDER + "kubernetes_resources_short_names.yml")
        if alert_name.lower() in short_names:
            return short_names[alert_name.lower()]
        return alert_name