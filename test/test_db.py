import psycopg2
from unittest import TestCase

from source.get_config import config
from source.create_DB import create_tables


class CreateDBTestCase(TestCase):
    """
    Test DB set up and import of data
    """
    # this needs to be called outside of set up so it is not called again for every test
    create_tables()

    def setUp(self):
        self.params = config()
        self.conn = psycopg2.connect(**params)
        self.cur = conn.cursor()

        # run create tables
        create_tables()

    def test_database_created(self):
        """Unit test to check redux database is created"""
        # check redux database has been created
        sql = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        self.cur.execute(sql)
        dbs = self.cur.fetchall()
        print(dbs)

        # assert database is there
        self.assertIn('redux', dbs)

    def test_persons_table(self):
        """Unit test to check persons table is created correctly"""
        sql = """
                SELECT column_name, data_type, character_maximum_length
                FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = persons; 
              """
        self.cur.execute(sql)
        table_info = self.cur.fetchall()
        print(table_info)





