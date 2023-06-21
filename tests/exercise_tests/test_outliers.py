"""
Don't change this file please. We'll use it to evaluate your submission
"""
import duckdb
import subprocess

import pytest


@pytest.fixture
def connection_to_db() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect("warehouse.db")
    return con


def run_outliers_calculation():
    result = subprocess.run(
        args=["python", "-m", "equalexperts_dataeng_exercise.outliers"],
        capture_output=True,
    )
    result.check_returncode()


def test_check_view_exists(connection_to_db):
    sql = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_type='VIEW' AND table_name='outlier_weeks' AND table_schema='blog_analysis';
    """
    run_outliers_calculation()
    result = connection_to_db.execute(sql)
    assert len(result.fetchall()) == 1, "Expected view 'outlier_weeks' to exist"


def test_check_view_has_data(connection_to_db):
    sql = "SELECT COUNT(*) FROM blog_analysis.outlier_weeks"
    run_outliers_calculation()
    result = connection_to_db.execute(sql)
    assert len(result.fetchall()) > 0, "Expected view 'outlier_weeks' to have data"
