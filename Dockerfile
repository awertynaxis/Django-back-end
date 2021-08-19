FROM python:3.8

ENV DEBIAN_FRONTEND=noninteractive
ADD . /opt/django_backend/
WORKDIR opt/django_backend/

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT [ "/bin/bash", "/opt/django_backend/entrypoint.sh" ]