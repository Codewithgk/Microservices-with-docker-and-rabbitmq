FROM ubuntu

RUN apt-get update 
RUN apt-get install -y libzmq3-dev python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install pika

COPY . /app

WORKDIR /app

ENTRYPOINT [ "python3" ]

CMD [ "logger.py" ]