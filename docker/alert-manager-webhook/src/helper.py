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
import json
from datetime import datetime
import yaml
from logconfigurator import LogConfigurator
from functools import reduce

log_config = None

def get_log_level():
    return os.getenv('LOG_LEVEL') if (os.getenv('LOG_LEVEL')) else "DEBUG"

def get_logger():
    global log_config

    if not log_config:
        log_config = LogConfigurator()
        return log_config.configure(get_log_level())

    log_config.set_level(get_log_level())
    return log_config.get_logger()

def load_yaml(file_path):
    get_logger().info("Loading YAML file: {}".format(file_path))
    with open(file_path) as file:
        return yaml.load(file, Loader=yaml.Loader)

def load_json(file_path):
    get_logger().info("Loading JSON file: {}".format(file_path))
    with open(file_path) as json_file:
        return json.load(json_file)

def convert_str_to_date(date_str):
    if date_str.rfind('.') != -1:
        date_str = date_str[0:date_str.rfind('.')]
    if date_str.rfind('Z') != -1:
        date_str = date_str[0:date_str.rfind('Z')]
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

def get_mapped_value(alert, mapping_keys):
    for key in mapping_keys:
        if isinstance(key, list):
            value = reduce(dict.get, key, alert)
            if value:
                return value