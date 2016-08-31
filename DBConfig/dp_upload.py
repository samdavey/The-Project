import pandas as pd
from sqlalchemy import create_engine

#enter filename, file extension, and local folder for required datafile
table_name = "phone_brand_device_model"
folder = "/The-Project/DBConfig/"
file_extension = ".csv" #Note: Currently script only supports .csv
path = folder+table_name+file_extension
print("Uploading: "+path)

#setup connection to AWS Postgres DB using sqlalchemy
engine = create_engine(r'postgresql://db_user:Rsummers1@my-postgres-db-instance.c79nyipdet5g.us-west-2.rds.amazonaws.com/test_db')

#List all tables in the database
tables = pd.read_sql("select relname as current_db_tables from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';",engine)
print(tables) 
print("\n")

#read in required datafile (replace "read_csv" with appropriate filetype)
df = pd.read_csv(path)
print("Pandas import complete: "+table_name)
#export the pandas dataframe to the Postgres DB, overwriting any existing table
df.to_sql(con=engine, name=table_name, if_exists='replace', flavor='postgres', chunksize=20000)
print("Postgres export complete: "+table_name) #NOTE: In testing, a 17kb file took 3 mins to export :(
#print first 10 rows from the DB as confirmation
print("Top 10 rows in Postgres table:\n")
output = pd.read_sql("select * from "+table_name+" limit 10",engine)
print(output)

#for reference: deprecated connection string using psycopg2:
#def connect():
#    conn = psycopg2.connect(host = "my-postgres-db-instance.c79nyipdet5g.us-west-2.rds.amazonaws.com",
#                            port = 5432,
#                            dbname = "test_db",
#                            user = "db_user",
#                            password = "Rsummers1")
#    c = conn.cursor()
#    return conn, c
#initialise connection
#conn, c = connect()
#engine.execute("DROP TABLE "+"test")