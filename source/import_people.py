import csv
import sys
import psycopg2
from config import config

def import_people():
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
            for row in reader:
                name = row.get('Name')
                tel = row.get('Tel')
                CLP = row.get('CLP')
                #for each line in the CSV, first create a group, if one doesn't exist
                if CLP:
                    sql = """INSERT INTO groups (group_name) VALUES (%s)
                    ON CONFLICT (group_name) DO NOTHING; """
                    cur.execute(sql, (CLP,))
                #retreive the group_id
                sql = """Select group_id from groups where group_name = (%s)"""
                cur.execute(sql, (CLP,))
                group_id = cur.fetchone()[0]
                #(really need to raise an exception here if no valid group ID is returned)
                #now create a person row in the database using the CSV row data and the group_id
                sql = """INSERT INTO persons (group_id, person_name, person_tel)
                VALUES (%s, %s, %s)"""
                cur.execute(sql, (group_id, name, tel,))
                print name, ' ', tel, ' ', CLP
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
    import_people()
