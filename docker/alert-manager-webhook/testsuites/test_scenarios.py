import os
import sys
import time
from pprint import pprint
import json

output = os.system("nohup python3 docker/eric-pm-alarm-handler-webhook/testsuites/dummy_webservice.py &")
print(output)

time.sleep(3)


def testsuite_send_notification_with_firing_status():
    output = os.popen("bash docker/eric-pm-alarm-handler-webhook/testsuites/send_firing_notification.sh").read().strip()
    print(output)
    b = json.loads("""
       {"additionalAttributes": {"additionalText": "attribute test"},
                        "eventType": "test",
                        "managedObjectInstance": "alarm type Test $",
                        "perceivedSeverity": "WARNING",
                        "probableCause": "test",
                        "recordType": "ALARM",
                        "specificProblem": "test"}
      """)
    with open('/var/tmp/data.txt') as f:
        data = json.load(f)
        pprint(data)
    if sorted(data.items()) == sorted(b.items()):
        assert data['perceivedSeverity'] == "WARNING"
        print("\n**** Case1 : Received expected transformed alert with perceivedSeverity as WARNING **** \n")
    else:
        print("\n**** Case1: Output is not equal to expected Output")
    file = open("/var/tmp/data.txt", "w")
    file.truncate(0)
    file.close()
    time.sleep(10)


def testsuite_send_notification_with_resolved_status():
    output = os.popen(
        "bash docker/eric-pm-alarm-handler-webhook/testsuites/send_resolved_notification.sh").read().strip()
    print(output)
    b = json.loads("""
        {"additionalAttributes": {"additionalText": "attribute test"},
                        "eventType": "test",
                        "managedObjectInstance": "alarm type Test $",
                        "perceivedSeverity": "CLEARED",
                        "probableCause": "test",
                        "recordType": "ALARM",
                        "specificProblem": "test"}
      """)

    with open('/var/tmp/data.txt') as f:
        data = json.load(f)
        pprint(data)
    if sorted(data.items()) == sorted(b.items()):
        assert data['perceivedSeverity'] == "CLEARED"
        print("\n**** Case2 : Received expected transformed alert with perceivedSeverity as cleared **** \n")
    else:
        print("\n**** Case2: Output is not equal to expected output")
    file = open("/var/tmp/data.txt", "w")
    file.truncate(0)
    file.close()
    time.sleep(10)


def testsuite__notification_with_missing_field():
    output = os.popen(
        "bash docker/eric-pm-alarm-handler-webhook/testsuites/send_fieldmissing_notification.sh").read().strip()
    print(output)
    b = json.loads("""
        {"additionalAttributes": {"additionalText": "attribute test"},
                        "eventType": "test",
                        "managedObjectInstance": "alarm type Test $",
                        "perceivedSeverity": "WARNING",
                        "probableCause": "test",
                        "recordType": "ALARM",
                        "specificProblem": "test"}
      """)
    assert os.path.getsize('/var/tmp/data.txt') == 0
    print("\n**** Case3: Transformed alert not received due to insufficient data.")
    time.sleep(10)