import psycopg2
import json
from datetime import date

from source.get_config import config

class redux_model(object):
    #Provides a Postgres redux data model

    def __init__(self):
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        self.conn = psycopg2.connect(**params)


    def list_campaigns(self, group_name):
        # get a list of campaigns for the group
        try:
            curr = self.conn.cursor()
            # find the Group ID from the group name
            sql = """SELECT group_id FROM groups WHERE group_name = (%s);"""
            curr.execute(sql, (group_name,))
            row = curr.fetchone()
            response = []
            if row:
                group_id = row[0]
                curr = self.conn.cursor()
                # get a list of active campaigns for the group ID
                today = str(date.today())
                sql = """SELECT * FROM campaigns WHERE group_id = (%s) and \
                campaign_start_date < (%s) and campaign_end_date > (%s);"""
                curr.execute(sql, (group_id, today, today))
                for row in curr:
                    response.append({'campaign_id': row[0],'campaign_name': row[2], \
                    'campaign_desc': row[3],'campaign_start_date': str(row[5]), \
                     'campaign_end_date': str(row[5]), 'campaign_global': row[6]})
            # return the list of campaigns or an empty list if there aren't any that match
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def get_next_member_to_call(self, campaign_name):
        # check the campaign exists then find a member in the campaign's group
        try:
            curr = self.conn.cursor()
            sql = """SELECT * FROM campaigns WHERE campaign_name = (%s)"""
            curr.execute(sql, (campaign_name,))
            row = curr.fetchone()
            if row:
                # start to build the JSON response with campaign data for the call
                response = {'campaign_id': row[0],'campaign_name': row[2], \
                'campaign_desc': row[3],'campaign_start_date': str(row[4]),\
                'campaign_end_date': str(row[5]),'campaign_global': row[6]}
                # find the first member without a row in the calls table for that
                # campaign
                sql = """SELECT * FROM members WHERE group_id = (%s)
                AND NOT EXISTS (SELECT call_id FROM calls WHERE campaign_id = (%s)
                AND member_id = members.member_id)"""
                curr.execute(sql, (row[1], row[0],))
                row = curr.fetchone()
                if row:
                    # complete building and then return the JSON call response
                    response.update({'member_id': row[0],'member_name': row[2],\
                     'member_tel': row[3]})
                    return response
                else:
                    return []
            else:
                return []
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def record_call_details (self, call_details):
        try:
            curr = self.conn.cursor()
            sql = """INSERT INTO calls (member_id, campaign_id, call_outcome,
                call_notes, call_date) VALUES (%s, %s, %s, %s, %s);"""
            curr.execute(sql, (call_details['member_id'], call_details['campaign_id'],\
                call_details['outcome'],call_details['notes'],\
                call_details['date']),)
            curr.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
