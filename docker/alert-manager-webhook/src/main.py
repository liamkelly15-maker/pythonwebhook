#!/usr/bin/python3

import json
import logging
import os

from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException
from alarm_handler_parser import AlarmHandlerParser
import helper

app = Flask(__name__)
flask_inbuilt_log = logging.getLogger('werkzeug')
flask_inbuilt_log.disabled = True


@app.route('/api/alertnotifications', methods=['POST'])
def webhook_api():
    """
        Rest endpoint to receive alert notification
    """
    if not request.is_json:
        logger.info('Non-JSON POST request received, Content-Type : {}'.format(request.headers['Content-Type']))
        abort(400)

    alert_notification = request.get_json()

    try:
        response = ah_parser.send_alarms(alert_notification)
    except Exception as e:
        logger.error(str(e))
    return response


@app.route('/-/healthy')
def healthy():
    """ To check liveness or health check"""
    logger.debug('API endpoint to check health status of AM Webhook accessed')
    return json.dumps(200)


@app.route('/-/ready')
def ready():
    """ To check readiness of application to receive traffic """
    logger.debug('API endpoint to check readiness of AM Webhook accessed')
    return json.dumps(200)


@app.errorhandler(HTTPException)
def handle_exception(error):
    """Return JSON instead of HTML for HTTP errors."""
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
    })
    response.content_type = "application/json"
    logger.error(response.data)
    return response


if __name__ == '__main__':
    ah_url = os.getenv('AH_URL') if (os.getenv('AH_URL')) else 'http://eric-fh-alarm-handler:6005/alarm-handler/v1beta1/fault-indications'
    http_port = int(os.getenv('HTTP_PORT')) if (os.getenv('HTTP_PORT')) else 49494
    logger = helper.get_logger()
    mapping_yaml = helper.load_yaml("/etc/opt/ericsson/mapping.yml")
    logger.info('Starting AM Webhook [port={}, loglevel={}, AHURL={}]'.format(http_port, helper.get_log_level(), ah_url))
    ah_parser = AlarmHandlerParser(ah_url, mapping_yaml)
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    app.run(host='0.0.0.0', port=http_port, debug=False)
    """
            I am not seeing where the AlarmHandlerParser object ah_parser calls its methods ????
        """