import psycopg2
from unittest import TestCase

from source.config import config
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
        self.cursor = conn.cursor()

    def test_create_tables(self):
        """Unit test for create_tables function"""
        # check redux database has been created
        sql = "SELECT datname FROM pg_database WHERE datistemplate = false;"
        dbs = self.cursor.execute(sql)
        print(dbs)

        #


