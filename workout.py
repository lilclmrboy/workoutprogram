#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import sqlite3 as lite
import sys

print ("Generating workout program")

con = lite.connect('test.db')

with con:

	con.row_factory = lite.Row
    
	cur = con.cursor()    
	cur.execute("SELECT * FROM Exercises")	
	rows = cur.fetchall()

	for row in rows:
		print "%s is %.0f percent of Clean and Jerk" %(row["Name"], 100.0 * row["PercentOfCleanAndJerk"])
