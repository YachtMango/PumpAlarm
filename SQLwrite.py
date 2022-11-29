datafileloc = "/home/mango3/Downloads/Pump Log File Epoch DT.csv"
dbloc = "/home/mango3/Documents/PumpAlarm/PumpAlarm/PClog.db"
import sqlite3
import pandas as pd

#set up db connection & open cursor
con = sqlite3.connect(dbloc)
cur = con.cursor()
cur.execute("CREATE TABLE pclog(Timestamp timestamp PRIMARY KEY,RT INTEGER,V REAL,Temp REAL)")

#load csv into Pandas 
logdata = pd.read_csv(datafileloc)
#load into sqlite db
logdata.to_sql('pclog',con ,if_exists='replace')


con.commit()
