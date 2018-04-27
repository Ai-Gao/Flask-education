FROM python:3.6
LABEL maintainer="Peng Xiao<xiaoquwl@gmail.com>"
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY . /simpledu/
WORKDIR /simpledu
EXPOSE 5000 80
CMD ['python','manage.py']
