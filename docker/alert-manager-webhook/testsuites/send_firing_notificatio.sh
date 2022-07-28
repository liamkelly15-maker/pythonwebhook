curl -X POST -H "Content-Type:application/json" http://localhost:49494/api/alertnotifications -d "{
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
}]}"