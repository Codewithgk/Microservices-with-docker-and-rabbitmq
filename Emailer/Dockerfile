FROM python:alpine3.7

WORKDIR /app

RUN pip3 install pika

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "emailer.py" ]