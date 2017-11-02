FROM python:3.5

# update apt get and get tools
RUN apt-get update && apt-get install -y nano \
                        less

# python pips
ADD ./requirements.txt /tmp/

# default pip
RUN pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt

ADD . /code/

WORKDIR /code

RUN chmod +x /code/*.sh

CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "source/create_DB.py"]
#CMD ["tail", "-F", "requirements.txt"]
