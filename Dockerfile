# now build main image and use all the installed packages
FROM python:3.7.1-slim
RUN apt-get -y update
RUN apt-get -y install curl
RUN apt-get -y install openssh-client git

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
ADD . .
CMD "bin/run"
