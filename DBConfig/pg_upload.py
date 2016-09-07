import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sys

#enter datafile information:
filename = "phone_brand_device_model"
folder = "/home/jovyan/work/_core/projects/datasets/talkingdata/"
file_extension = ".csv" #Note: Currently script only supports .csv
path = folder+filename+file_extension

#enter db connection information:
host = "my-postgres-db-instance.c79nyipdet5g.us-west-2.rds.amazonaws.com"
port = 5432
dbname = "test_db"
user = "db_user"
password = "Rsummers1" 

#defining function for db connection using psycopg2:
def connect():
    conn = psycopg2.connect(host = host,
                            port = port,
                            dbname = dbname,
                            user = user,
                            password = password)
    try:
    	c = conn.cursor()
    except:
    	print("DB connection failed")
    	exit(1)
    return conn, c

#perform file import/table creation
print("\n***Commencing file upload***")
try:
	engine = create_engine(r"postgresql://"+user+":"+password+"@"+host+"/"+dbname)
	print("Creating table...")
	df = pd.read_csv(path, nrows=0)
	df.to_sql(con=engine, name=filename, if_exists='replace')
	print("Successfully created table: "+filename)
except:
	print("Unable to import: "+filename+file_extension)
	print(sys.exc_info())
	exit(1)

#initialise connection
conn, c = connect()

#export the csv to the db, removing any pre-existing tables
try: 
	print("Transferring data...")
	#copy data from the csv, ignoring the header row
	file = open(path, 'r')
	#upload data to the DB table, removing the 'index' column created by pandas
	c.execute("ALTER TABLE "+filename+" DROP COLUMN index;")
	c.copy_from(file, filename,sep=',')
	c.execute("DELETE FROM "+filename+" WHERE ctid = '(0,1)';")

	print("Successfully transferred: "+filename)
except:
	print(sys.exc_info())
	exit(1)
print("***file upload complete***")

#Print out the first 5 rows to confirm correct import
try:
	#output = pd.read_sql("select * from "+filename+" limit 5",engine)
	c.execute("select * from "+filename+" limit 5",engine)
	print("\nHere are the top 5 rows for inspection:\n")
	print(c.fetchall())
except:
	print("Unable to reconnect to table: "+filename)
	exit(1)

#commit the table changes and close the DB connection
conn.commit()
conn.close()	