FROM debian

LABEL Author="SumanDeb"
LABEL ImageOwner="MLS"

RUN apt-get update && \
    apt-get install curl -y &&  \
    apt-get install python -y  && \
    apt-get install python-pip -y

ENV KUBERNETES_API_SERVER_HOST="kubernetes.svc.local"
ENV KUBERNETES_API_SERVER_PORT="443"

ADD get_events.py  /usr/local/bin/
RUN chmod +x /usr/local/bin/

CMD ["python", "/usr/local/bin/get_events.py"]

