FROM python:3.8.16-bullseye

WORKDIR /iron_dome

RUN pip3 install --upgrade pip
RUN pip3 install argparse
RUN pip3 install watchdog
RUN pip3 install python-daemon
RUN pip3 install psutil

COPY ./irondome.py ./irondome.py

COPY ./utils/entrypoint.sh ./entrypoint.sh

RUN mkdir /data

ENTRYPOINT [ "sh", "entrypoint.sh" ]
# CMD [ "python3" , "irondome.py", "--path", "/data"]
# CMD [ "sleep", "infinity" ]