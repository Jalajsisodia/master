import duckdb


def create_schema_blog_analysis(connection):
    try:
        
        result = connection.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'blog_analysis'")
        schema_exists = bool(result.fetchone())

        if not schema_exists:
            # Create the schema 'blog_analysis'
            connection.execute("CREATE SCHEMA blog_analysis")
            print("Schema 'blog_analysis' created successfully.")
        else:
            print("Schema 'blog_analysis' already exists.")

    except Exception as e:
        print("An error occurred:", str(e))


def create_table_votes(connection):
    
    try:     
        
        table_name = 'votes' 
        schema = 'blog_analysis'
        table_schema = '''
        CREATE  TABLE {schema}.{table_name} (
            Id INTEGER,
            PostId INTEGER,
            VoteTypeId INTEGER,
            CreationDate timestamp
        )
        '''
           

        result = connection.execute(f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table_name}' AND table_schema='{schema}'")
        table_exists = bool(result.fetchone())

        if table_exists:
            print(f"Table '{table_name}' exists.")
        else:
            connection.execute(table_schema.format(table_name=table_name, schema = schema))
            print(f"Table '{table_name}' Created SuccessFully.")
    except Exception as e:
        print("An error occurred:", str(e))


def create_db_warehouse_connection():
    try:
        connection = duckdb.connect(database='warehouse.db', read_only=False)
        
        return connection
    except Exception as e:
        print("An error occurred:", str(e))

connection = create_db_warehouse_connection()

create_schema_blog_analysis(connection)

create_table_votes(connection)

connection.close()