curl -XPOST "http://localhost:49494/api/alertnotifications" -H 'Content-Type: application/json' -d '{
   "receiver": "web\\.hook",
   "status": "resolved",
   "alerts": [
      {
         "status": "resolved",
         "labels": {
            "alertname": "Deployment",
            "app_kubernetes_io_instance": "eric-oss-common-base",
            "app_kubernetes_io_managed_by": "Helm",
            "app_kubernetes_io_name": "eric-pm-kube-state-metrics",
            "app_kubernetes_io_version": "2.1.0_10",
            "chart": "eric-pm-kube-state-metrics-2.1.0_10",
            "deployment": "eric-log-transformer",
            "instance": "192.168.69.53:8080",
            "job": "eric-pm-kube-state-metrics",
            "kubernetes_name": "eric-pm-kube-state-metrics",
            "kubernetes_namespace": "eric-eo-cm-ci406",
            "namespace": "eric-eo-cm-ci406",
            "severity": "Warning"
         },
         "annotations": {
            "description": "Deployment Replicas mismatch, desired value does not match..",
            "summary": "Kubernetes Deployment Replicas Mismatch"
         },
         "startsAt": "2022-07-29T11:13:27.3Z",
         "endsAt": "2022-07-29T11:17:27.3Z",
         "generatorURL": "/metrics/viewer/graph?g0.expr=kube_deployment_spec_replicas%7Bnamespace%3D%22eric-eo-cm-ci406%22%7D+%21%3D+kube_deployment_status_replicas_available%7Bnamespace%3D%22eric-eo-cm-ci406%22%7D&g0.tab=1",
         "fingerprint": "fbab788ec4c1018b"
      }
   ],
   "groupLabels": {
      "alertname": "Deployment"
   },
   "commonLabels": {
      "alertname": "Deployment",
      "app_kubernetes_io_instance": "eric-oss-common-base",
      "app_kubernetes_io_managed_by": "Helm",
      "app_kubernetes_io_name": "eric-pm-kube-state-metrics",
      "app_kubernetes_io_version": "2.1.0_10",
      "chart": "eric-pm-kube-state-metrics-2.1.0_10",
      "deployment": "eric-log-transformer",
      "instance": "192.168.69.53:8080",
      "job": "eric-pm-kube-state-metrics",
      "kubernetes_name": "eric-pm-kube-state-metrics",
      "kubernetes_namespace": "eric-eo-cm-ci406",
      "namespace": "eric-eo-cm-ci406",
      "severity": "Warning"
   },
   "commonAnnotations": {
      "description": "Deployment Replicas mismatch, desired value does not match..",
      "summary": "Kubernetes Deployment Replicas Mismatch"
   },
   "externalURL": "http://localhost:9093",
   "version": "4",
   "groupKey": "{}:{alertname=\"Deployment\"}",
   "truncatedAlerts": 0
}'