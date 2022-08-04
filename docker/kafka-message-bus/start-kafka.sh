#!/bin/bash -ex
#copy in a custom server.properties
echo "starting the kafka broker server"
exec opt/kafka/bin/kafka-server-start.sh /server.properties