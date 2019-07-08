FROM debian

LABEL Author="SumanDeb"
LABEL ImageOwner="MLS"

RUN apt-get update && \
    apt-get install curl -y &&  \
    apt-get install python -y  && \
    apt-get install python-pip -y && \
    apt-get install jq -y && \
    apt-get install vim -y



ENV KUBERNETES_API_SERVER_HOST="kubernetes.svc.local"
ENV KUBERNETES_API_SERVER_PORT="443"

ADD get_events.sh  /usr/local/bin/
RUN chmod +x /usr/local/bin/

CMD ["/bin/sh", "/usr/local/bin/get_events.sh"]

