datafileloc = "/home/mango3/Downloads/Pump Log File Clean.csv"
import sqlite3
import datetime
import pandas as pd

#set up db connection & open cursor
con = sqlite3.connect("PClog.db")
cur = con.cursor()
#cur.execute("CREATE TABLE pclog(Timestamp timestamp PRIMARY KEY,Day TEXT,Date date ,Time time,ComboDT TEXT,RT INTEGER,V REAL,Temp REAL)")

#load csv into Pandas 
logdata = pd.read_csv(datafileloc)
#load into sqlite db
logdata.to_sql('pclog',con ,if_exists='replace')


con.commit()