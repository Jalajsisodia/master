import duckdb

def create_view_outlier_weeks(connection):

    connection.execute("SET SCHEMA 'blog_analysis'")
    connection.sql("""
                    CREATE OR REPLACE VIEW OUTLIER_WEEKS AS(
                    WITH weekly_votes AS (
                    SELECT
                        YEAR(CreationDate) AS Year,
                        CASE WHEN WEEK(CreationDate) in (52,53) AND MONTH(CreationDate) = 1 THEN 0 ELSE WEEK(CreationDate) END AS WeekNumber,
                        COUNT(*) AS VoteCount,
                        AVG(COUNT(*)) OVER () AS AvgVoteCount
                    FROM votes
                    GROUP BY (CreationDate)
                    )
                    SELECT
                    Year,
                    WeekNumber,
                    VoteCount,
                    FROM weekly_votes
                    WHERE ABS(VoteCount - AvgVoteCount) > (AvgVoteCount * 0.2)) """)
    
    # connection.sql("""
    #                 SELECT COUNT(*) FROM blog_analysis.outlier_weeks  """).show()
    
def create_db_warehouse_connection():
    try:
        connection = duckdb.connect(database='warehouse.db', read_only=False)
        
        return connection
    except Exception as e:
        print("An error occurred:", str(e))

connection = create_db_warehouse_connection()
    
create_view_outlier_weeks(connection)
