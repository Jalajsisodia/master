import unittest
from unittest.mock import patch
import duckdb
import sys
sys.path.insert(0, 'F:\EqualExperts\equal-experts-moot-unstuffy-upswing-4565fef52da6\equalexperts_dataeng_exercise')
from outliers import create_view_outlier_weeks


class TestDbOutliersView(unittest.TestCase):

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

    def test_create_schema_blog_analysis(self):
        create_view_outlier_weeks(self.connection)
        result = self.connection.execute("SELECT COUNT(*) FROM blog_analysis.outlier_weeks")
        schema_exists = bool(result.fetchone())
        self.assertTrue(schema_exists)

if __name__ == '__main__':
    unittest.main()