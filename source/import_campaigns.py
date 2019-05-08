import csv
import sys
import psycopg2
from datetime import datetime

from get_config import config


def import_campaigns(csv_path):
    """
    Import campaign from CSV into database
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
        start_date = datetime.strptime(row.get('Start Date'), '%d/%m/%Y')
        end_date = datetime.strptime(row.get('End Date'), '%d/%m/%Y')
        globalString = row.get('Global')

        if name and group and desc and start_date and end_date:

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
                # if group id not present, add to groups table
                group_sql = """
                            INSERT INTO groups (group_name) VALUES (%s);
                            SELECT group_id FROM groups WHERE group_name = (%s);
                            """
                cur.execute(group_sql, (group, group,))

                group_id = cur.fetchone()[0]

            #now insert the campaign row using the CSV row data plus the group_id
            sql = """INSERT INTO campaigns (campaign_name, group_id, campaign_desc,
            campaign_start_date, campaign_end_date, campaign_global) VALUES (%s,%s,%s,%s,%s, %s)"""
            cur.execute(sql, (name, group_id, desc, start_date, end_date, isGlobal,))
            #(really need to raise an exception here if the insert fails)
            print (name, ' ', group, ' ', desc, ' ', start_date, ' ', end_date, ' ', globalString)


    cur.close()

    # commit the changes
    conn.commit()

if __name__ == '__main__':
    import_campaigns()
