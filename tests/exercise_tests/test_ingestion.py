"""
Don't change this file please. We'll use it to evaluate your submission
"""
import os
import subprocess

import duckdb
import pytest


@pytest.fixture
def cursor():
    if os.path.exists("warehouse.db"):
        os.remove("warehouse.db")
    try:
        cursor = duckdb.connect("warehouse.db")
        yield cursor
    finally:
        cursor.close()


def run_ingestion():
    result = subprocess.run(
        args=[
            "python",
            "-m",
            "equalexperts_dataeng_exercise.ingest",
            "uncommitted/votes.jsonl",
        ],
        capture_output=True,
    )
    result.check_returncode()


def test_check_table_exists(cursor):
    run_ingestion()
    sql = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_type='BASE TABLE' AND table_name='votes' AND table_schema='blog_analysis';
    """
    result = cursor.sql(sql)
    assert len(result.fetchall()) == 1, "Expected table 'votes' to exist"


def count_rows_in_data_file():
    with open("uncommitted/votes.jsonl", "r", encoding="utf-8") as data:
        return sum(1 for _ in data)


def test_check_correct_number_of_rows_after_ingesting_once(cursor):
    sql = "SELECT COUNT(*) FROM blog_analysis.votes"
    run_ingestion()
    result = cursor.execute(sql)
    count_in_db = result.fetchall()[0][0]
    assert (
        count_in_db <= count_rows_in_data_file()
    ), "Expect only as many entries in votes as lines in the data file"


def test_check_correct_number_of_rows_after_ingesting_twice(cursor):
    sql = "SELECT COUNT(*) FROM blog_analysis.votes"
    run_ingestion()
    run_ingestion()
    result = cursor.execute(sql)
    count_in_db = result.fetchall()[0][0]
    assert (
        count_in_db <= count_rows_in_data_file()
    ), "Expect only as many entries in votes as lines in the data file"
