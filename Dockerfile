FROM python:3-alpine

RUN mkdir -p /opt/reflection
ADD requirements.txt /opt/reflection
ADD reflection.py /opt/reflection
ADD install.sh /opt/reflection
ADD run.sh /
RUN chmod +x /run.sh

RUN chmod +x /opt/reflection/install.sh
RUN cd /opt/reflection; ./install.sh

RUN mkdir /data
VOLUME /data
EXPOSE 8080

ENTRYPOINT ./run.sh