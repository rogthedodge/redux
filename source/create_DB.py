#!/usr/bin/python
import time
import psycopg2
from os.path import dirname

from get_config import config
from import_campaigns import import_campaigns
from import_members import import_members
from import_users import import_users


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """DROP TABLE IF EXISTS groups CASCADE;""",
        """DROP TABLE IF EXISTS members CASCADE;""",
        """DROP TABLE IF EXISTS campaigns CASCADE;""",
        """DROP TABLE IF EXISTS calls CASCADE;""",
        """DROP TABLE IF EXISTS users CASCADE;""",
        """DROP TYPE IF EXISTS outcome;""",
        """CREATE TABLE groups (
            group_id SERIAL PRIMARY KEY,
            group_name VARCHAR(255) NOT NULL UNIQUE
        );""",
        """CREATE TABLE members (
            member_id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            member_name VARCHAR(255) NOT NULL,
            member_tel VARCHAR(30),
            FOREIGN KEY (group_id)
            REFERENCES groups (group_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );""",
        """CREATE TABLE campaigns (
            campaign_id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            campaign_name VARCHAR(255) NOT NULL,
            campaign_desc VARCHAR(255) NOT NULL,
            campaign_start_date TIMESTAMP,
            campaign_end_date TIMESTAMP,
            campaign_global BOOLEAN,
            FOREIGN KEY (group_id)
            REFERENCES groups (group_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );""",
        """CREATE TYPE outcome AS ENUM ('SKIPPED', 'UNANSWERED', 'ANSWERED');""",
        """CREATE TABLE calls (
            call_id SERIAL PRIMARY KEY,
            member_id INTEGER NOT NULL,
            campaign_id INTEGER NOT NULL,
            call_outcome outcome NOT NULL,
            call_notes VARCHAR(255),
            call_date TIMESTAMP NOT NULL,
            FOREIGN KEY (member_id)
            REFERENCES members (member_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (campaign_id)
            REFERENCES campaigns (campaign_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );""",
        """CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_email VARCHAR(255),
            user_CLP VARCHAR(255)
        );"""
        ]

    # need to sleep for a few seconds to allow postgres container to start up
    time.sleep(10)

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
    import_members(dirname(dirname(__file__)) + '/code/test/test_members.csv')
    import_campaigns(dirname(dirname(__file__)) + '/code/test/test_campaigns.csv')
    import_users(dirname(dirname(__file__)) + '/code/test/test_users.csv')
