import csv
import sqlite3
from sqlite3 import Error


conn = sqlite3.connect(r".\ofppt.db")


#create table ofppt (niveau TEXT,filiere TEXT,groupe TEXT,annee TEXT, cin TEXT, nom TEXT, prenom TEXT, absence INTEGER )
cur = conn.cursor()

cur.execute("select distinct groupe from ofppt")
print(cur.fetchall())

conn.commit()
conn.close()
