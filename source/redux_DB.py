import psycopg2
from config import config
import json

class redux_model(object):

    #Provides a Postgres redux data model

    def __init__(self):
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        self.conn = psycopg2.connect(**params)

    def get_person(self, event_name):
        # check the event exists then find a person in the event's group
        try:
            curr = self.conn.cursor()
            sql = """SELECT group_id FROM events WHERE event_name = (%s);"""
            curr.execute(sql, (event_name,))
            row = curr.fetchone()
            if row:
                # for now, just return any person in the group. We're going to need
                # to find the next person without a row in the calls table for that
                # event, or where the outcome on the call entry is 'engaged/no answer'
                sql = """SELECT * FROM persons WHERE group_id = (%s);"""
                curr.execute(sql, (row,))
                row = curr.fetchone()
                if row:
                    return {'person_name': row[2], 'person_tel': row[3]}
                else:
                    return {'error': 'no more people to call for event'}
            else:
                return {'error': 'no such event'}
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
