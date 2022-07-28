#!bin/bash
#the body must be in " " and escape all the quotes with \ - not sure why this is required
curl -X POST -H "Content-Type:application/json" http://localhost:49494/api/alertnotifications -d "{
   \"receiver\":\"webhook\",
   \"status\":\"firing\",
   \"alerts\":[
      {
         \"status\":\"firing\",
         \"labels\":{
            \"alertname\":\"High Pod Memory\",
            \"severity\":\"slack\"
         },
         \"annotations\":{
            \"summary\":\"High Memory Usage\"
         },
         \"startsAt\":\"2022-07-26T19:55:58.97Z\",
         \"endsAt\":\"0001-01-01T00:00:00Z\",
         \"generatorURL\":\"http://prometheus-deployment-87cc8fb88-4kgsr:9090/graph?g0.expr=sum%28container_memory_usage_bytes%29+%3E+1&g0.tab=1\",
         \"fingerprint\":\"f74798f72524fe89\"
      }
   ],
   \"groupLabels\":{
      \"alertname\":\"High Pod Memory\"
   },
   \"commonLabels\":{
      \"alertname\":\"High Pod Memory\",
      \"severity\":\"slack\"
   },
   \"commonAnnotations\":{
      \"summary\":\"High Memory Usage\"
   },
   \"externalURL\":\"http://alertmanager-78dfd7464f-tdfv9:9093\",
   \"version\":\"4\",
   \"groupKey\":\"{}/{}:{alertname=\"High Pod Memory\"}\",
   \"truncatedAlerts\":0
}"