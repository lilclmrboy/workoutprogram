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
    (1, 'Clean and Jerk', 1.0, "kg", "Olympic, Clean"),
    (2, 'Snatch', 0.8, "kg", "Olympic, Snatch"),
    (3, 'Bench Press', 1.0, "kg", "Strength"),
    (4, 'Clean', 1.0666, "kg", "Olympic, Clean"),
    (5, 'Clean High Pull', 1.3, "kg", "Pull"),
    (6, 'Clean Pull', 1.3, "kg", "Pull"),
    (7, 'Clean from Knees', 0.95, "kg", "Olympic, Clean"),
    (8, 'Jerk Rack', 1.10, "kg", "Olympic, Jerk"),
    (9, 'Push Jerk', 1.0, "kg", "Olympic, Jerk"),
    (10, 'Jerk Recover', 1.20, "kg", "Olympic, Jerk"),
    (11, 'Back Squat', 1.40, "kg", "Strength, Squat"),
    (12, 'Front Squat', 1.224, "kg", "Strength, Squat"),
    (13, 'Overhead Squat', 0.88, "kg", "Olympic, Strength, Squat"),
    (14, 'Sit-ups', 100.0, "reps", "Core"),
    (15, 'Crunches', 100.0, "reps", "Core"),
    (16, 'Press', 0.75, "kg", "Strength, Press"),
    (17, 'Push Press', 0.825, "kg", "Strength, Press"),
    (18, 'Press Behind Neck', 0.825, "kg", "Strength, Press"),
    (19, 'Curls', 0.5, "kg", "Strength")
)

users_prs = (
    (1, 'Matt', 'Krugman', 95.0, "kg", 1.0, "Clean and Jerk", "2016-02-18", ""),
    (2, 'Matt', 'Krugman', 75.0, "kg", 1.0, "Snatch", "2016-02-18", ""),
    (3, 'Matt', 'Krugman', 150.0, "kg", 1.0, "Deadlift", "2016-02-18", ""),
	(4, 'Matt', 'Krugman', 143.0, "kg", 1.0, "Back Squat", "2016-02-18", ""),
)

con = lite.connect('test.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Exercises")
    cur.execute("DROP TABLE IF EXISTS UserRecords")
    cur.execute("CREATE TABLE Exercises(Id INT, Name TEXT, PercentOfCleanAndJerk REAL, Units TEXT, Type TEXT)")
    cur.execute("CREATE TABLE UserRecords(Id INT, FirstName TEXT, LastName TEXT, Record REAL, Units TEXT, Reps REAL, Exercise TEXT, Date TEXT, Notes TEXT)")
    cur.executemany("INSERT INTO Exercises VALUES(?, ?, ?, ?, ?)", activities)
    cur.executemany("INSERT INTO UserRecords VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", users_prs)
    
#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed
#
# import sqlite3 as lite
# import sys
#
print ("Generating workout program")

con = lite.connect('test.db')

with con:

    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Exercises")
    rows = cur.fetchall()

    for row in rows:
        if (row["Units"] == "kg"):
            print "%s is %.0f percent of Clean and Jerk" %(row["Name"], 100.0 * row["PercentOfCleanAndJerk"])

    cur.execute("SELECT * FROM Exercises WHERE Type like '%Core%'")
    rows = cur.fetchall()

    for row in rows:
        print("Found exercise that matches type Core: %s" % row["Name"])
        
    cur.execute("SELECT * FROM UserRecords")
    rows = cur.fetchall()	
    
    for row in rows:
    	print row

con.close()
