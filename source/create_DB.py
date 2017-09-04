#!/usr/bin/python

import psycopg2
from config import config


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
        """CREATE TABLE calls (
            call_id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            call_outcome VARCHAR(255) NOT NULL,
            call_notes VARCHAR(255) NOT NULL,
            call_date TIMESTAMP,
            FOREIGN KEY (person_id)
            REFERENCES persons (person_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (event_id)
            REFERENCES events (event_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );"""
        ]

    conn = None
    try:
        # read the connection parameters
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
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
