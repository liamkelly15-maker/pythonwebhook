import os
import sys
from datetime import datetime
from unittest import TestCase
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from alarm_handler_parser import FaultIndicationBuilder
import helper

RES_FOLDER = os.path.join(os.path.dirname(__file__), "resources") + os.path.sep
MAPPING_YAML_PATH = RES_FOLDER + "mapping.yml"
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(Z|[\+-]\d{2}:\d{2})+')


class TestFaultIndicationBuilder(TestCase):

    def test_replicas_mismatch_alert(self):
        print("TEST-STARTED: Replica Mismatch Alert parsing")
        mapping = helper.load_yaml(MAPPING_YAML_PATH)
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "replicas_mismatch_alert_request.json")
        expected_fault_response = helper.load_json(RES_FOLDER + "replicas_mismatch_alert_response.json")
        actual_fault_response = []
        for alert in request['alerts']:
            fault_indication = fi_builder.build(alert)
            actual_fault_response.append(fault_indication)
        self.assertEqual(expected_fault_response, actual_fault_response, "Fail to parse Replica Mismatch Alert")
        print("TEST-FINISHED: Replica Mismatch Alert parsed successfully")

    def test_communication_error_alert(self):
        print("TEST-STARTED: Communication Error Alert parsing")
        mapping = helper.load_yaml(MAPPING_YAML_PATH)
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "communication_error_alert_request.json")
        expected_fault_response = helper.load_json(RES_FOLDER + "communication_error_alert_response.json")
        actual_fault_response = []
        for alert in request['alerts']:
            fault_indication = fi_builder.build(alert)
            actual_fault_response.append(fault_indication)
        self.assertEqual(expected_fault_response, actual_fault_response, "Fail to parse Communication Error Alert")
        print("TEST-FINISHED: Communication Error Alert parsed successfully")

    def test_misconfigured_mapped_field_should_be_skipped(self):
        print("TEST-STARTED: Misconfigured mapped field should be skipped")
        mapping = helper.load_yaml(RES_FOLDER + "misconfigured_mapping.yml")
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "replicas_mismatch_alert_request.json")
        expected_fault_response = helper.load_json(RES_FOLDER + "misconfigured_mapping_response.json")
        actual_fault_response = []
        for alert in request['alerts']:
            fault_indication = fi_builder.build(alert)
            actual_fault_response.append(fault_indication)
        self.assertEqual(expected_fault_response, actual_fault_response, "Fail to skip misconfigured mapped field")
        print("TEST-FINISHED: Misconfigured mapped field parsed successfully")

    def test_empty_required_fields_should_return_default_value(self):
        print("TEST-STARTED: Empty required fields should return default value")
        mapping = helper.load_yaml(MAPPING_YAML_PATH)
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "empty_required_fields_alert_request.json")
        expected_created_at = datetime.now()
        fault_indication = fi_builder.build(request['alerts'][0])
        self.assertEqual('UNKNOWN', fault_indication['faultName'], "Fail to set default value for [faultName]")
        self.assertEqual('UNKNOWN', fault_indication['serviceName'], "Fail to set default value for [serviceName]")
        date_pattern.match(fault_indication['createdAt'])
        actual_created_at = helper.convert_str_to_date(fault_indication['createdAt'])
        delta_time = expected_created_at - actual_created_at
        self.assertLess(delta_time.total_seconds(), 30, "Fail to set current time for [createdAt]")
        self.assertEqual(0, fault_indication['expiration'], "Fail to set default value for [expiration]")
        print("TEST-FINISHED: Empty required fields parsed successfully")

    def test_fault_name_custom_parser(self):
        print("TEST-STARTED: Fault Name Custom Parser")
        mapping = helper.load_yaml(RES_FOLDER + "custom_fault_name_parser_mapping.yml")
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "custom_fault_name_parser_request.json")
        expected_fault_response = helper.load_json(RES_FOLDER + "custom_fault_name_parser_response.json")
        actual_fault_response = []
        for alert in request['alerts']:
            fault_indication = fi_builder.build(alert)
            actual_fault_response.append(fault_indication)
        self.assertEqual(expected_fault_response, actual_fault_response, "Fail to parse with Fault Name Custom Parser")
        print("TEST-FINISHED: Custom Field Parser executed successfully")

    def test_misconfigured_date_should_return_default_value(self):
        print("TEST-STARTED: Misconfigured date should return default value")
        mapping = helper.load_yaml(RES_FOLDER + "misconfigured_date_mapping.yml")
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "replicas_mismatch_alert_request.json")
        expected_created_at = datetime.now()
        fault_indication = fi_builder.build(request['alerts'][0])
        date_pattern.match(fault_indication['createdAt'])
        actual_created_at = helper.convert_str_to_date(fault_indication['createdAt'])
        delta_time = expected_created_at - actual_created_at
        self.assertLess(delta_time.total_seconds(), 30, "Fail to set current time for [createdAt]")
        self.assertEqual(0, fault_indication['expiration'], "Fail to set default value for [expiration]")
        fault_indication = fi_builder.build(request['alerts'][1])
        self.assertEqual(60, fault_indication['expiration'], "Fail to set default value for [expiration]")
        print("TEST-FINISHED: Misconfigured date executed successfully")

    def test_missing_required_fields_in_mapping_should_return_default_value(self):
        print("TEST-STARTED: Missing required fields in mapping should return default")
        mapping = helper.load_yaml(RES_FOLDER + "missing_required_fields_mapping.yml")
        fi_builder = FaultIndicationBuilder(mapping)
        request = helper.load_json(RES_FOLDER + "replicas_mismatch_alert_request.json")
        expected_created_at = datetime.now()
        fault_indication = fi_builder.build(request['alerts'][0])
        self.assertEqual('UNKNOWN', fault_indication['faultName'], "Fail to set default value for [faultName]")
        self.assertEqual('UNKNOWN', fault_indication['serviceName'], "Fail to set default value for [serviceName]")
        date_pattern.match(fault_indication['createdAt'])
        actual_created_at = helper.convert_str_to_date(fault_indication['createdAt'])
        delta_time = expected_created_at - actual_created_at
        self.assertLess(delta_time.total_seconds(), 30, "Fail to set current time for [createdAt]")
        print("TEST-FINISHED: Missing required fields in mapping executed successfully")