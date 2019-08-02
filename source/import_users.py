import csv
import sys
import psycopg2

from get_config import config

def import_users(csv_path):
    conn = None
    CSVFile = open(csv_path, 'rt')
    reader = csv.DictReader(CSVFile)

    # read the connection parameters
    params = config()

    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    for row in reader:
        email = row.get('Email')
        CLP = row.get('CLP')

        sql = """INSERT INTO users (user_email, user_CLP) VALUES (%s, %s)"""
        cur.execute(sql, (email, CLP,))
        print (email, ' ', CLP)
    cur.close()
    # commit the changes
    conn.commit()

if __name__ == '__main__':
    import_users()
