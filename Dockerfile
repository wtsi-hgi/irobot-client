FROM python:3.6

WORKDIR /irobotclient

ADD /irobotclient /irobotclient
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD "/bin/bash"