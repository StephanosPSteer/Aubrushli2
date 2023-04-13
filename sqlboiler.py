import sqlite3
import pandas as pd
from pathboiler import pathboiler

class sqlboiler:

    
    def getpaths(self):
        pb = pathboiler()
        current_dir, db_path = pb.getkeypaths()
    
        return current_dir, db_path
    def openconscur(self):
        current_dir, db_path = self.getpaths()
        conn = sqlite3.connect(db_path)
        return conn

    def closeconn(self,conn):
        conn.commit()
        conn.close()


    def getstyle(self): 
        conn = self.openconscur()
        currstyle = pd.read_sql_query("SELECT StylesheetPath FROM settings", conn)
        self.closeconn(conn)
        #just return the style string rightnow
        return currstyle.iloc[0]["StylesheetPath"]

    def getallproduction(self):
        conn = self.openconscur()
        prods = pd.read_sql_query("SELECT * from production", conn)
        self.closeconn(conn)
        return prods

    def getshotlist(self, prodid):
        conn = self.openconscur()
        #print(prodid)
        shotlist  = pd.read_sql_query("SELECT * FROM Shotlists where productionid=?", conn, params=(prodid,))
        self.closeconn(conn)
        #just returning shotlistpath right now - revisit if need to return more
        return shotlist.iloc[0]["ShotlistPath"], shotlist.iloc[0]["PreferredSeed"], shotlist.iloc[0]["numberofimages"], shotlist.iloc[0]["ShotlistImagesFolder"]