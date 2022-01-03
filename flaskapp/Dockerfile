FROM python:alpine3.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5001

ENTRYPOINT [ "python3" ]

CMD [ "mainapp.py" ]