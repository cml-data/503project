FROM ubuntu:latest

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt-get -y install libpq-dev gcc
RUN python3 -m pip install pandas
RUN python3 -m pip install requests
RUN python3 -m pip install psycopg2
RUN python3 -m pip install sqlalchemy
RUN ln -s /usr/bin/python3 /usr/bin/python

ADD weather.py /

CMD [ "python", "./weather.py" ]