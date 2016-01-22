import urllib2
import yaml
from datetime import datetime
from crontab import CronTab

###
	# Function to find the first game time of the day
	# A cron job will then be scheduled for this time
	# This will be used to collect the rosters for every fantasy team
	# since rosters generally lock after the first game of the day starts 
###

url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/master_scoreboard.json".format(datetime.now().year, '{:02d}'.format(datetime.now().month), '{:02d}'.format(datetime.now().day))

response = urllib2.urlopen(url)
games = yaml.safe_load(response)

# Get the first game of the day and store the time and time zone 
firstGameTime = games["data"]["games"]["game"][0]["time"]

timePieces = firstGameTime.split(":")

firstGameHour = int(timePieces[0])
firstGameMinutes = timePieces[1]

# Convert the hour to Central Time
if firstGameHour >= 10:
	firstGameHour = firstGameHour - 1
else:
	firstGameHour = firstGameHour + 11

cron = CronTab(user='root')

job = cron.new(command='python /home/pi/Python/LineupAlert/GetStartingPlayers.py')

job.setall('{0} {1} * * *'.format(firstGameMinutes, firstGameHour))

job.enable()
cron.write()
