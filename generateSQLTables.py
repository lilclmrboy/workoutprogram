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
    (1,  'Back Squat'             , 1.45    , "kg"  , "Strength, Squat"),
    (2,  'Bench Press'            , 1.0     , "kg"  , "Strength"),
    (3,  'Climbing'               , 45.0    , "yos" , "Climbing"),
    (4,  'Clean and Jerk'         , 1.0     , "kg"  , "Olympic, Clean"),
    (5,  'Clean'                  , 1.0666  , "kg"  , "Olympic, Clean"),
    (6,  'Clean High Pull'        , 1.3     , "kg"  , "Pull"),
    (7,  'Clean Pull'             , 1.3     , "kg"  , "Pull"),
    (8,  'Clean from Knees'       , 0.95    , "kg"  , "Olympic, Clean"),
    (9,  'Crunches'               , 100.0   , "reps", "Core"), 
    (10, 'Curls'                  , 0.5     , "kg"  , "Strength"),  
	(11, 'Deadlift'               , 1.8     , "kg"  , "Strength"),
    (12, 'Front Squat'            , 1.224   , "kg"  , "Strength, Squat"),	
    (13, 'Jerk Behind Neck'       , 1.00    , "kg"  , "Olympic, Jerk"), 
    (14, 'Jerk Recover'           , 1.20    , "kg"  , "Olympic, Jerk-Stability"), 
    (15, 'Jerk Rack'              , 1.10    , "kg"  , "Olympic, Jerk"),
    (16, 'Manual Situps'          , 10.0    , "reps", "Partner"),
    (17, 'Overhead Squat'         , 0.88    , "kg"  , "Olympic, Strength, Olymipic-Squat"), 
    (18, 'Plank'                  , 120.0   , "sec" , "Core"),
    (19, 'Press'                  , 0.75    , "kg"  , "Strength, Press"),
    (20, 'Press Behind Neck'      , 0.825   , "kg"  , "Strength, Press"),
    (21, 'Power Clean'            , 0.825   , "kg"  , "Clean, Olympic"),
    (22, 'Power Snatch'           , 0.66    , "kg"  , "Snatch, Olympic"),
    (23, 'Pull ups'               , 10.0    , "reps", "Core, Strength"),
    (24, 'Push Jerk'              , 1.0     , "kg"  , "Olympic, Jerk"),
    (25, 'Push Press'             , 0.825   , "kg"  , "Strength, Press"),
    (26, 'Push ups'               , 50.0    , "reps", "Strength, Core"),
    (27, 'Sit-ups'                , 60.0   , "reps", "Core"),
    (28, 'Snatch'                 , 0.8     , "kg"  , "Olympic, Snatch"),
    (29, 'Snatch Drop'            , 0.85    , "kg"  , "Olympic, Snatch"),
    (30, 'Weighted Vest Plank'    , 0.18    , "kg"  , "Core"),
    (31, '2 Position Clean'       , 0.825   , "kg"  , "Olympic, Clean"),
    (32, '3 Position Clean'       , 0.8     , "kg"  , "Olympic, Clean"),
    (33, '2 Position Power Clean' , 0.78    , "kg"  , "Olympic, Clean"),
    (34, 'Ab Rollout'             , 50.0    , "reps", "Core"), 
    (35, 'Hanging Leg Raise'      , 25.0    , "reps", "Core"), 

)

# users_prs = (
#     (1, 'Matt', 'Krugman', 97.5, "kg", 1.0, "Clean and Jerk", "2016-02-18", ""),
#     (2, 'Matt', 'Krugman', 77.5, "kg", 1.0, "Snatch", "2016-02-18", ""),
#     (3, 'Matt', 'Krugman', 160.0, "kg", 1.0, "Deadlift", "2016-02-18", ""),
# 	(4, 'Matt', 'Krugman', 170.0, "kg", 1.0, "Back Squat", "2016-02-18", ""),
# 	(5, 'Matt', 'Krugman', 69.0,  "yos", 1.0, "Climbing", "2016-02-18", ""),
# )

users_prs = (
    (1, 'Matt', 'Krugman', 90.0, "kg", 1.0, "Clean and Jerk", "2016-11-26", ""),
    (2, 'Kim', 'Krugman', 40.0, "kg", 1.0, "Clean and Jerk", "2018-11-26", ""),
)

con = lite.connect('test.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Exercises")
    cur.execute("DROP TABLE IF EXISTS UserRecords")
    cur.execute("CREATE TABLE Exercises(Id INT, Name TEXT, PercentOfCleanAndJerk REAL, Units TEXT, Type TEXT)")
    cur.execute("CREATE TABLE UserRecords(Id INT, FirstName TEXT, LastName TEXT, PR REAL, Units TEXT, Reps REAL, Exercise TEXT, Date TEXT, Notes TEXT)")
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
        
    cur.execute("SELECT * FROM UserRecords WHERE Exercise is '%Power Snatch%'")
    rows = cur.fetchall()	
    
    print "--------------------------"
    
    if (len(rows) == 0):
    	print "No exericse %s found" % "Power Snatch"
    
    print "--------------------------"
    for row in rows:
    	print row

con.close()
