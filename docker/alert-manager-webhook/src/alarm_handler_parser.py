
import json
import requests
from requests.exceptions import RequestException
import helper
from fault_indication_builder import FaultIndicationBuilder


class AlarmHandlerParser:

    def __init__(self, ah_url, mapping):

        self.logger = helper.get_logger()
        self.ah_url = ah_url
        self.fi_builder = FaultIndicationBuilder(mapping)

    def send_alarms(self, alert_notification):
        """
            Sends alarms to alarm handler endpoint provided as env variable.

        """
        self.logger.info('Received notification from alertmanager: {}'.format(alert_notification))
        try:

            for alert in alert_notification['alerts']:
                ah_service = AlarmHandlerService(self.logger)
                fm_alarm = self.fi_builder.build(alert)
                if fm_alarm:
                    status_code = ah_service.post_alarm(self.ah_url, json.dumps(fm_alarm))
                    if status_code // 100 != 2:
                        return "Error", status_code
                else:
                    return "Bad Request", 400
        except Exception as e:
            self.logger.error(
                "Request failed to process due to invalid data from client side with exception:{}".format(str(e)))
            return "Bad Request", 400
        return "Success", 200


class AlarmHandlerService:

    def __init__(self, logger):
        self.logger = logger

    def post_alarm(self, ah_url, fault_indication):
        """
        Post request to alarm handler rest service
        Headers provided here are mandatory

        """
        self.logger.info("Sending request to Alarm Handler endpoint: {}".format(ah_url))

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        try:
            response = requests.post(ah_url, data=fault_indication, headers=headers)
            self.logger.debug("Received status code from Alarm Handler service: {} ".format(response.status_code))
            if response.status_code == 204:
                self.logger.info(
                    'Request processed successfully, alarm has been sent to Alarm Handler service: {}'.format(
                        fault_indication))
                self.logger.debug("Received content from Alarm Handler service: {} ".format(response.text))
                return 204
            else:
                self.logger.error(
                    'Rest API call failed to post data to Alarm Handler service due to HTTP error:{}'.format(
                        response.status_code))
                self.logger.error("Received content from Alarm Handler service: {} ".format(response.text))
                return response.status_code
        except RequestException as r:
            self.logger.error(str(r))
            self.logger.error(
                "Rest API call failed to post data to Alarm Handler service due to connection error: {}".format(
                    fault_indication))
            return 502