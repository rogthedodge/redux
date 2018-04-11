import psycopg2
import json

from source.get_config import config

class redux_model(object):
    #Provides a Postgres redux data model

    def __init__(self):
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        self.conn = psycopg2.connect(**params)

    def get_next_person_to_call(self, event_name):
        # check the event exists then find a person in the event's group
        try:
            curr = self.conn.cursor()
            sql = """SELECT * FROM events WHERE event_name = (%s);"""
            curr.execute(sql, (event_name,))
            row = curr.fetchone()
            if row:
                # start to build the JSON response with event data for the call
                response = {'event_id': row[0],'event_name': row[2], \
                'event_desc': row[3],'event_date': str(row[4]), 'event_global': row[5]}
                # find the first person without a row in the calls table for that
                # event
                sql = """SELECT * FROM persons WHERE group_id = (%s)
                AND NOT EXISTS (SELECT call_id FROM calls WHERE event_id = (%s)
                AND person_id = persons.person_id)"""
                curr.execute(sql, (row[1], row[0],))
                row = curr.fetchone()
                if row:
                    # complete building and then return the JSON call response
                    response.update({'person_id': row[0],'person_name': row[2],\
                     'person_tel': row[3]})
                    return response
                else:
                    return {'error': 'no more people to call for event'}
            else:
                return {'error': 'no such event'}
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def record_call_details (self, call_details):
        try:
            curr = self.conn.cursor()
            sql = """INSERT INTO calls (person_id, event_id, call_outcome,
                call_notes, call_date) VALUES (%s, %s, %s, %s, %s);"""
            curr.execute(sql, (call_details['person_id'], call_details['event_id'],\
                call_details['outcome'],call_details['notes'],\
                call_details['date']),)
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
