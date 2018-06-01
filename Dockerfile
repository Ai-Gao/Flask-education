FROM python:3.6
LABEL maintainer="Peng Xiao<xiaoquwl@gmail.com>"
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY . /simpledu/
WORKDIR /simpledu
EXPOSE 5000 80
CMD gunicorn -k flask_sockets.worker -b 127.0.0.1:5000 manage:app 
