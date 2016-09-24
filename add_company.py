#!/usr/bin/python
from DbConnection import DBConnection

db = DBConnection('127.0.0.1', 'root', 'root', 'market_analysis')
res = db.select_in_db("SELECT * FROM company")
print res
db.close_connection()
