#!/usr/bin/env python
from LineupFunctions import *

#Get a list of new players that are out of the lineup today
OutPlayers = GetNewOutOfLineupPlayers()

if len(OutPlayers) > 0:
	SendAlerts(OutPlayers)
