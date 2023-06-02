FROM python:3.11-rc-slim

RUN apt update && apt -y install procps net-tools sysstat
RUN pip install argparse
RUN pip install watchdog
RUN pip install python-daemon
RUN pip install psutil

WORKDIR /iron_dome
COPY ./irondome.py ./irondome.py

COPY ./utils/entrypoint.sh ./entrypoint.sh

RUN mkdir /data

ENTRYPOINT [ "sh", "entrypoint.sh" ]