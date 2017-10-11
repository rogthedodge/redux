import csv
import sys
import psycopg2
from config import config
from datetime import datetime

def import_events():
    conn = None
    CSVFile = open(sys.argv[1], 'rt')
    try:
        reader = csv.DictReader(CSVFile)
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            #import each line in the csv
            for row in reader:
                name = row.get('Name')
                group = row.get('Group')
                desc = row.get('Description')
                date = datetime.strptime(row.get('Date'), '%d/%m/%Y')
                globalString = row.get('Global')
                if name and group and desc and date:
                    if globalString == 'Yes' or 'yes': isGlobal = True
                    #first find the group_id from the group name
                    sql = """Select group_id from groups where group_name = (%s)"""
                    cur.execute(sql, (group,))
                    group_id = cur.fetchone()[0]
                    #(really need to raise an exception here if no valid group ID is returned)
                    #now insert the person row using the CSV row data plus the group_id
                    sql = """INSERT INTO events (event_name, group_id, event_desc,
                    event_date, event_global) VALUES (%s,%s,%s,%s,%s)"""
                    cur.execute(sql, (name, group_id, desc, date, isGlobal,))
                    #(really need to raise an exception here if the insert fails)
                    print (name, ' ', group, ' ', desc, ' ', date, ' ', globalString)
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if conn is not None:
            conn.close()
        CSVFile.close()

if __name__ == '__main__':
    import_events()
