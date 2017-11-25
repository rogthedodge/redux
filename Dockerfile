FROM python:3.5

# update apt get and get tools
RUN apt-get update && apt-get install -y nano \
                        less

# python pips
ADD ./requirements.txt /tmp/

# default pip
RUN pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt
RUN pip install config configparser psycopg2 datetime falcon gunicorn httpie

ADD . /code/

WORKDIR /code

RUN chmod +x /code/*.sh

#CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "source/create_DB.py"]
#CMD ["./wait-for-it.sh", "postgres:5432", "--", "tail", "requirements.txt"]
#ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", ":8000", "source.redux_API:api"]
