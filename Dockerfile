FROM python:3.8

WORKDIR /app

ARG ACCESS_TOKEN

ENV ACCESS_TOKEN ${ACCESS_TOKEN}

COPY requirements.txt requirements.txt

RUN pip3 install pip update

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=8080"]