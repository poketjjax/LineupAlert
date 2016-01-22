#!/usr/bin/env python
import urllib2
import smtplib
from bs4 import BeautifulSoup
import psycopg2

def scrapePlayers(contactInfo, teamLinks):
	fantasyPlayers = []
	for team in teamLinks:
		if team:
			fantasyPage = urllib2.urlopen(team).read()			
			fantasyTeam = BeautifulSoup(fantasyPage)
			
			players = fantasyTeam.select('#playertable_0 tr.pncPlayerRow td.playertablePlayerName a[tab="null"]')
			
			insert = """INSERT INTO "LineupAlertOwnedPlayers" ("PlayerName", "ContactInfo", "TeamLink") VALUES """
			
			for player in players:
				if player.text not in fantasyPlayers:
					fantasyPlayers.append(player.text)
					insert += "('{0}', '{1}', '{2}'),".format(player.text, contactInfo, team)
			
			cur.execute(insert[:-1])
			conn.commit()

try:
	conn = psycopg2.connect("dbname=dingers_Dingers user=dingers_dingers host=198.58.94.152 password=")
	cur = conn.cursor()
except:
	print "Unable to connect to the database"
	
cur.execute("""DELETE FROM "LineupAlertOwnedPlayers" """)
	
cur.execute("""SELECT * FROM "LineupAlertOwners" """)
				
rows = cur.fetchall()

for row in rows:
	contactInfo = row[1]
	teamLinks = [row[2], row[3], row[4], row[5], row[6]]
	scrapePlayers(contactInfo, teamLinks)

conn.commit()
cur.close()
conn.close()	



