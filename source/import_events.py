import csv
import sys
import psycopg2
from config import config
from datetime import datetime

def import_events(csv_path):
    """
    Import event from CSV into database
    :param csv_path |str: path to CSV
    :return: None
    """
    conn = None
    CSVFile =  open(csv_path, 'rt')
    reader = csv.DictReader(CSVFile)

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

            if globalString in ['Yes', 'yes', 'y', 'Y']:
                isGlobal = True
            else:
                isGlobal = False

            #first find the group_id from the group name
            sql = """Select group_id from groups where group_name = (%s);"""
            cur.execute(sql, (group,))

            # check if group id is returned
            if cur.rowcount:
                group_id = cur.fetchone()[0]
            else:
                # if group id not present isn't, add to groups table
                group_sql = """
                            INSERT INTO groups (group_name) VALUES (%s);
                            SELECT group_id FROM groups WHERE group_name = (%s);
                            """
                cur.execute(group_sql, (group, group,))

                group_id = cur.fetchone()[0]

            #now insert the person row using the CSV row data plus the group_id
            sql = """INSERT INTO events (event_name, group_id, event_desc,
            event_date, event_global) VALUES (%s,%s,%s,%s,%s)"""
            cur.execute(sql, (name, group_id, desc, date, isGlobal,))
            #(really need to raise an exception here if the insert fails)
            print (name, ' ', group, ' ', desc, ' ', date, ' ', globalString)

    cur.close()
    
    # commit the changes
    conn.commit()

if __name__ == '__main__':
    import_events()
