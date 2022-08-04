#dockerfile image name   zookeeper
#i got awful issues with weird characters in the bash start-zk.sh so i insatlled the dos2unix
#change file properties - line separators to Unix ... and remove the dos2unix use
FROM openjdk:8
USER root

ENV ZK_HOME=/zookeeper
ENV ZK_DATA_DIR=/var/lib/zookeeper/data
ENV ZK_DATA_LOG_DIR=/var/lib/zookeeper/log
ENV ZK_LOG_DIR=/var/log/zookeeper
ENV ZK_CLIENT_PORT=2181
ENV ZK_SERVER_PORT=2888
ENV ZK_ELECTION_PORT=3888


ARG ZK_VERSION=3.7.0
ARG ZK_URL=https://archive.apache.org/dist/zookeeper/zookeeper-${ZK_VERSION}/apache-zookeeper-${ZK_VERSION}-bin.tar.gz

ARG ZK_DIST=apache-zookeeper-${ZK_VERSION}-bin

EXPOSE $ZK_CLIENT_PORT $ZK_SERVER_PORT $ZK_ELECTION_PORT

#create a symbolix link from zookeeper version to /opt/zookeeper
#this link allows you to run scripts in the apache version by referencing the symbolic link e.g. exec /opt/zookeeper/bin/zkServer.sh
# then when an update of version takes place the code does not change

RUN set -x \
   && curl -k -L -o ${ZK_DIST}.tar.gz ${ZK_URL} \
   && tar -xzf "$ZK_DIST.tar.gz" -C /opt \
   && rm -r "$ZK_DIST.tar.gz" \
   && ln -s /opt/$ZK_DIST /opt/zookeeper
#   && rm -rf /opt/zookeeper/lib/commons-cli-*.jar \
#   && rm -rf /opt/zookeeper/lib/*log4j* \
#   && rm -rf /opt/zookeeper/lib/*jackson* \
#   && rm -rf /opt/zookeeper/lib/*jetty* \
#   && rm -rf /opt/zookeeper/lib/*slf4j-api*

# Create a user for the zookeeper process and configure file system ownership
RUN echo "101493:x:101493:101493:An Identity for eric-data-coordinator-zk:/home/zookeeper:/bin/bash" >> /etc/passwd
RUN echo "101493:!::0:::::" >>/etc/shadow

#RUN set -x \
#    && mkdir -p $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR /usr/share/zookeeper /tmp/zookeeper /usr/etc/ /etc/zookeeper/secrets /opt/zookeeper/config-dynamic/ \
#    && chown -R 101493:0 $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR /usr/share/zookeeper /tmp/zookeeper /usr/etc/ /etc/zookeeper/secrets /opt/zookeeper/config-dynamic/ \
#    && chmod -R g+rwx $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR /usr/share/zookeeper /tmp/zookeeper /usr/etc/ /etc/zookeeper/secrets /opt/zookeeper/config-dynamic/ \
#    && chmod -R g=u $ZK_DATA_DIR $ZK_DATA_LOG_DIR $ZK_LOG_DIR /usr/share/zookeeper /tmp/zookeeper /usr/etc/ /etc/zookeeper/secrets /opt/zookeeper/config-dynamic/ \
#    && ln -s /opt/zookeeper/conf/ /usr/etc/zookeeper \
#    && ln -s /opt/zookeeper/bin/* /usr/bin \
#    && ln -s /opt/zookeeper/lib/* /usr/share/zookeeper


COPY start-zk.sh /
RUN chmod +x /start-zk.sh
#RUN dos2unix /start-zk.sh


ENTRYPOINT ["/bin/bash","./start-zk.sh"]
#ENTRYPOINT ["/bin/bash", "-c"]
