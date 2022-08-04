#dockerfile image name   kafka
#i got awful issues with weird characters in the bash start-zk.sh so i insatlled the dos2unix
#change file properties - line separators to Unix ... and remove the dos2unix use
FROM openjdk:11
USER root


ARG KAFKA_VERSION=3.0.0
ARG SCALA_VERSION=2.13
ARG KAFKA_URL=https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

ARG KAFKA_DIST=kafka_${SCALA_VERSION}-${KAFKA_VERSION}


#RUN apt-get update && apt-get install dos2unix

#i comment out wget as I downloaded to local to speed up imgae build
#RUN mkdir /kafka
#RUN wget -qO - ${KAFKA_REPO}${KAFKA_NAME} | tar xzf --directory ${KAFKA_HOME}

#ADD kafka_2.13-3.2.0.tgz / .
#RUN tar -xvf /kafka_2.13-3.2.0.tgz -C /kafka

RUN set -x \
   && curl -k -L -o ${KAFKA_DIST}.tgz ${KAFKA_URL} \
   && tar -xzf "$KAFKA_DIST.tgz" -C /opt \
   && rm -r "$KAFKA_DIST.tgz" \
   && ln -s /opt/$KAFKA_DIST /opt/kafka


#RUN set -x \
#   && curl -k -L -o /tmp/kafka.tgz ${KAFKA_URL} \
#   && cd /tmp/ \
#   && mkdir /kafka \
#   && mkdir -p /var/log/kafka \
#   && tar xfz kafka.tgz -C /opt --strip-components 1 \
#   && ln -s /opt/$ZK_FOLDER /opt/zookeeper
#   && mkdir -p /usr/share/java/kafka \
#   && cd kafka/bin \
#   && find -type f -name '*.sh' | while read f; do cp "$f" "${f%.sh}"; done \
#   && cd /tmp
#   && cp -R kafka/bin/* /usr/bin/ \
#   && cp -R kafka/libs/* /usr/share/java/kafka/ \
#   && ln -s /usr/share/java/kafka /usr/libs \
#   && ln -s /var/log/kafka /usr/logs \
#   && ln -s /etc/kafka /usr/config \

COPY server.properties /

COPY start-kafka.sh /
RUN chmod +x /start-kafka.sh
#RUN dos2unix /start-zk.sh


EXPOSE 9092

ENTRYPOINT ["/bin/bash","-c","./start-kafka.sh"]
#ENTRYPOINT ["/bin/bash", "-c"]
