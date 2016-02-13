#!/usr/bin/python
# -*- coding: utf-8 -*-
# See: http://zetcode.com/db/sqlitepythontutorial/
# for tips

import sqlite3 as lite
import sys

# Exercise description tables
#   ExerciseType m_type;
#  int m_weightmax;
#  int m_time;
#  bool m_optional;
#  int m_nSets;
#  int m_nSetsConsolidated;
#  int m_sets[EXERCISE_SETS_MAX][3];
#  float m_fRatio;

print ("Generating exercise tables")

activities = (
    (1, 'Clean and Jerk', 1.0, "kg"),
    (2, 'Snatch', 0.8, "kg"),
    (3, 'Bench Press', 1.0, "kg"),
    (4, 'Clean', 1.0666, "kg"),
    (5, 'Clean High Pull', 1.3, "kg"),
    (6, 'Clean Pull', 1.3, "kg"),
    (7, 'Clean from Knees', 0.95, "kg")
)

con = lite.connect('test.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Exercises")
    cur.execute("CREATE TABLE Exercises(Id INT, Name TEXT, PercentOfCleanAndJerk REAL), Units TEXT")
    cur.executemany("INSERT INTO Exercises VALUES(?, ?, ?, ?)", activities)

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed
# 
# import sqlite3 as lite
# import sys
#
# print ("Generating workout program")
#
# con = lite.connect('test.db')
#
# with con:
#
# 	con.row_factory = lite.Row
#
# 	cur = con.cursor()
# 	cur.execute("SELECT * FROM Exercises")
# 	rows = cur.fetchall()
#
# 	for row in rows:
# 		print "%s is %.0f percent of Clean and Jerk" %(row["Name"], 100.0 * row["PercentOfCleanAndJerk"])
