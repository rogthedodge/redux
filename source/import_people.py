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
                CLP = row.get('CLP')
                if CLP:
                    sql = """INSERT INTO groups (group_name) VALUES (%s)
                    ON CONFLICT (group_name) DO NOTHING; """
                    cur.execute(sql, (CLP,))
                    print CLP
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
