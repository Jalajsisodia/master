import unittest
import duckdb
import sys
sys.path.insert(0, 'F:\EqualExperts\equal-experts-moot-unstuffy-upswing-4565fef52da6\equalexperts_dataeng_exercise')
from db import create_schema_blog_analysis, create_table_votes

class TestDbSchemaCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = cls.create_db_warehouse_connection()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    @staticmethod
    def create_db_warehouse_connection():
        try:
            connection = duckdb.connect(database='warehouse.db', read_only=False)
            return connection
        except Exception as e:
            print("An error occurred:", str(e))

    def setUp(self):
        self.connection.execute("DROP SCHEMA IF EXISTS blog_analysis CASCADE")

    def test_create_schema_blog_analysis(self):
        create_schema_blog_analysis(self.connection)
        result = self.connection.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'blog_analysis'")
        schema_exists = bool(result.fetchone())
        self.assertTrue(schema_exists)

    def test_create_table_votes(self):
        create_schema_blog_analysis(self.connection)  # Ensure schema exists
        create_table_votes(self.connection)
        result = self.connection.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'votes' AND table_schema = 'blog_analysis'")
        table_exists = bool(result.fetchone())
        self.assertTrue(table_exists)

if __name__ == '__main__':
    unittest.main()
