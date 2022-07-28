#dockerfile name   alert-manager-webhook
FROM python:3
USER root
#the python:3 base has pip
RUN pip install --no-cache-dir https://github.com/pallets/flask/archive/2.1.0.tar.gz https://github.com/psf/requests/archive/v2.24.0.zip pyyaml
#i was getting a flask error so reduced the version of werkzeug
RUN pip install "werkzeug<2.1.0"

COPY ./src /etc/opt/ericsson/alert-manager-webhook
COPY image_content/pipe_fifo.sh /usr/local/bin/pipe_fifo.sh

RUN chmod 755 /usr/local/bin/pipe_fifo.sh; chmod 755 /etc/opt/ericsson/alert-manager-webhook/*

EXPOSE 49494
#ENTRYPOINT ["/usr/local/bin/pipe_fifo.sh","/etc/opt/ericsson/alert-manager-webhook/main.py"]
CMD ["/etc/opt/ericsson/alert-manager-webhook/main.py"]
ENTRYPOINT ["python"]

# the flask webserver should keep the script running