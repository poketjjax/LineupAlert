#!/usr/bin/env python
import psycopg2

try:
	conn = psycopg2.connect("dbname=dingers_Dingers user=dingers_dingers host=198.58.94.152 password=udunno11")
	cur = conn.cursor()
except:
	print "Unable to connect to the database"

cur.execute("""DELETE FROM "LineupAlertOutPlayers" """)

conn.commit()
cur.close()
conn.close()
