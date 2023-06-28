import json
import sys
import duckdb

def check_if_raw_file_exists():
    try:
        file_to_load = sys.argv[1]
        with open(file_to_load) as votes_in:
            for line in votes_in:
                print(json.loads(line))
                break
        # Calling function to transform votes file    
        wrtie_transform_json_to_load(file_to_load)
    except FileNotFoundError:
        print("Please download the dataset using 'poetry run exercise fetch-data'")

def wrtie_transform_json_to_load(file_to_load):

    output_file = "transformed_votes.jsonl"
    columns_to_extract = ['Id', 'PostId', 'VoteTypeId', 'CreationDate']
    extracted_data = []
    with open(file_to_load, 'r') as file:    
        for line in file:
            try:
                record = json.loads(line)
                extracted_record = {column: record.get(column) for column in columns_to_extract}
                extracted_data.append(extracted_record)            
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {str(e)}")
    try:
        with open(output_file, 'w') as file:
            for extracted_record in extracted_data:
                formatted_record = json.dumps(extracted_record, separators=(',', ':'))
                file.write(formatted_record + '\n')         
    except FileNotFoundError:
        print("transformed file not found'")

    #function to ingesting transformed file into table   
    ingest_data_into_votes_table()


def ingest_data_into_votes_table():
    
    output_file = "transformed_votes.jsonl"
    connection = duckdb.connect(database='warehouse.db', read_only=False)    
    try:
        #Cleaning Table to avoid duplicate insertion
        connection.execute("SET SCHEMA 'blog_analysis'")    
        connection.execute("DELETE FROM votes")

        load_data = "COPY votes FROM '{}' (FORMAT JSON)".format(output_file)
        connection.execute(load_data)

        result = connection.execute("SELECT count(*) FROM votes")
        records_count = result.fetchone()

        print(records_count[0], "Records loaded successfully")

        connection.close()
    except Exception as e:
        print("An error occurred in Copy:", str(e))

check_if_raw_file_exists()
