import psycopg2
import json

from get_config import config

class redux_model(object):

    #Provides a Postgres redux data model

    def __init__(self):
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        self.conn = psycopg2.connect(**params)

    def get_next_call(self, event_name):
        # check the event exists then find a person in the event's group
        try:
            curr = self.conn.cursor()
            sql = """SELECT * FROM events WHERE event_name = (%s);"""
            curr.execute(sql, (event_name,))
            row = curr.fetchone()
            if row:
                # start to build the JSON response with event data for the call
                # beginning with the date field because it needs unpacking
                response = {'event_name': row[2], 'event_desc': row[3], \
                'event_date': str(row[4]), 'event_global': row[5]}
                # find the first person without a row in the calls table for that
                # event
                sql = """SELECT * FROM persons WHERE group_id = (%s)
                AND NOT EXISTS (SELECT call_id FROM calls WHERE event_id = (%s)
                AND person_id = persons.person_id)"""
                curr.execute(sql, (row[1], row[0],))
                row = curr.fetchone()
                if row:
                    # complete building and then return the JSON call response
                    response.update({'person_name': row[2], 'person_tel': row[3]})
                    return response
                else:
                    return {'error': 'no more people to call for event'}
            else:
                return {'error': 'no such event'}
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
