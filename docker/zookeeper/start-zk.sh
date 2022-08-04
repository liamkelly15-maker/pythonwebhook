#!/bin/sh

# Start zookeeper
#if [ "$LOG_OUTPUT" == "stream" ]; then
#    /usr/bin/stdout-redirect -redirect file -logfile /logs/datacoordinatorzk.log -container datacoordinatorzk -service-id $SERVICE_ID -run="/opt/zookeeper/bin/zkStart.sh"
#elif [ "$LOG_OUTPUT" == "all" ]; then
#    /usr/bin/stdout-redirect -redirect all -logfile /logs/datacoordinatorzk.log -container datacoordinatorzk -service-id $SERVICE_ID -run="/opt/zookeeper/bin/zkStart.sh"
#else
    exec /opt/zookeeper/bin/zkServer.sh start-foreground
#fi