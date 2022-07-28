#!bin/bash
curl --location --request POST 'http://localhost:49494/api/alertnotifications' \
--header 'Content-Type: text/plain' \
--data-raw '"{
       \"alerts\":[{
       \"status\": \"firing\",
       \"labels\": {
               \"alertname\": \"ContainerHighThrottleRate\",
               \"service\": \"my-service\",
               \"severity\":\"WARNING\",
               \"instance\": \"$name.example.net\",
               \"specificProblem\": \"test\",
               \"probableCause\": \"test\",
               \"eventType\": \"test\",
               \"recordType\": \"ALARM\",
               \"managedObjectInstance\": \"alarm type Test $\"
     },
       \"annotations\": {
           \"summary\": \"samplr\",
           \"description\": \"sample\",
           \"additionalText\": \"attribute test\"

       },
       \"generatorURL\": \"http://prometheus.int.example.net/<generating_expression>\",
       \"startsAt\":\"$startDate\"
}]}"'