#!/usr/bin/python
import time
import psycopg2
from os.path import dirname
from config import config
from import_events import import_events
from import_people import import_people


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """DROP TABLE IF EXISTS groups CASCADE;""",
        """DROP TABLE IF EXISTS persons CASCADE;""",
        """DROP TABLE IF EXISTS events CASCADE;""",
        """DROP TABLE IF EXISTS calls CASCADE;""",
        """CREATE TABLE groups (
            group_id SERIAL PRIMARY KEY,
            group_name VARCHAR(255) NOT NULL UNIQUE
        );""",
        """CREATE TABLE persons (
            person_id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            person_name VARCHAR(255) NOT NULL,
            person_tel VARCHAR(30),
            FOREIGN KEY (group_id)
            REFERENCES groups (group_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );""",
        """CREATE TABLE events (
            event_id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            event_name VARCHAR(255) NOT NULL,
            event_desc VARCHAR(255) NOT NULL,
            event_date TIMESTAMP,
            event_global BOOLEAN,
            FOREIGN KEY (group_id)
            REFERENCES groups (group_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );"""
        """CREATE TYPE outcome AS ENUM ('SKIP', 'UNANSWERED', 'ANSWERED');"""
        """CREATE TABLE calls (
            call_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            call_outcome outcome NOT NULL,
            call_notes VARCHAR(255),
            call_date TIMESTAMP NOT NULL,
            FOREIGN KEY (person_id)
            REFERENCES persons (person_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (event_id)
            REFERENCES events (event_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );"""
        ]

    # need to sleep for 5 seconds to allow postgres container to start up
    time.sleep(5)

    #read the connection parameters
    params = config()

    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    # create table one by one
    for command in commands:
        cur.execute(command)

    # close communication with the PostgreSQL database server
    cur.close()
    conn.close()


if __name__ == '__main__':
    create_tables()
    import_people(dirname(dirname(__file__)) + 'test_people.csv')
    import_events(dirname(dirname(__file__)) + 'test_events.csv')

