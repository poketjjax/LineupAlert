#!/usr/bin/env python
import urllib2
import json
import yaml
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
import psycopg2
import requests

def GetNewOutOfLineupPlayers():
	# Get list of players who are sitting out that are already in the DB
	try:
		conn = psycopg2.connect("dbname=dingers_Dingers user=dingers_dingers host=198.58.94.152 password=udunno11")
		cur = conn.cursor()
	except:
		print "Unable to connect to the database"
		
	cur.execute("""SELECT "PlayerName" FROM "LineupAlertOutPlayers" """)
	
	rows = cur.fetchall()
	rows = [i[0] for i in rows]
	
	# Get full list of players sitting out from fantasy pros website
	fullList = []
	soup = BeautifulSoup(urllib2.urlopen("http://www.fantasypros.com/mlb/lineup-alerts/today"))

	hittersTable = soup.select('div.hitters-list table tbody tr td')[1::3]

	for player in hittersTable:
		if "DL15" not in player.text and "DL60" not in player.text and "DL7" not in player.text:
			fullList.append(str(player.find('a').text))

	# Get list of players who are sitting out, but aren't in the DB yet
	newOutPlayers = [player for player in fullList if player not in rows]
	
	# Insert the new sitting out players into the DB
	if len(newOutPlayers) > 0:
		cur.execute("""INSERT INTO "LineupAlertOutPlayers" VALUES ('{0}')  """.format("'),('".join(newOutPlayers)))
		conn.commit()
	
	cur.close()
	conn.close()
	
	return newOutPlayers
	
def SendAlerts(OutPlayers):
	try:
		conn = psycopg2.connect("dbname=dingers_Dingers user=dingers_dingers host=198.58.94.152 password=udunno11")
		cur = conn.cursor()
	except:
		print "Unable to connect to the database"
	
	cur.execute("""SELECT "ContactInfo", "PlayerName", "TeamLink" FROM "LineupAlertOwnedPlayers" WHERE "PlayerName" IN ('{0}') """.format('\', \''.join(OutPlayers)))
	rows = cur.fetchall()
	
	if len(rows) > 0:
		# At least 1 person owns a player who is sitting out
		for player in rows:
			SendMessage(player)
			
	cur.close()
	conn.close()
					
def SendMessage(playerInfo):
	sender = 'lineupalert@gmail.com'
	receivers = playerInfo[0]
	shortURL = goo_shorten_url(playerInfo[2])
	
	message = "\n\n{0} is out of the lineup. \n\nEdit your lineup here:\n{1}".format(playerInfo[1], shortURL)

	# Use smtp and gmail credentials to send out message
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login('lineupalert@gmail.com', 'lineup11')
	server.sendmail(sender, receivers, message)         
	server.close()	
	
def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?fields=id&key=AIzaSyDGH5YYSzcXd0_3KZj97Sumkvt7wEjG-5Y'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    
    request = requests.post(post_url, data=json.dumps(payload), headers=headers)
    
    return json.loads(request.text)['id']
    
    
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
