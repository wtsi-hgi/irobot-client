FROM python:3.6

RUN mkdir /irobotclient
WORKDIR /irobotclient


ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
RUN python setup.py install

EXPOSE 5000

CMD "/bin/bash"