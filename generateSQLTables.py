#!/usr/bin/python
# -*- coding: utf-8 -*-
# See: http://zetcode.com/db/sqlitepythontutorial/
# for tips

import sqlite3 as lite
import sys

#define mCLIMBING_5p2 9
#define mCLIMBING_5p3 12
#define mCLIMBING_5p4 15
#define mCLIMBING_5p5 18
#define mCLIMBING_5p6 21
#define mCLIMBING_5p7 24
#define mCLIMBING_5p8m 27
#define mCLIMBING_5p8 30
#define mCLIMBING_5p8p 33
#define mCLIMBING_5p9m 36
#define mCLIMBING_5p9 39
#define mCLIMBING_5p9p 42
#define mCLIMBING_5p10a 45
#define mCLIMBING_5p10b 48
#define mCLIMBING_5p10c 51
#define mCLIMBING_5p10d 54
#define mCLIMBING_5p11a 57
#define mCLIMBING_5p11b 60
#define mCLIMBING_5p11c 63
#define mCLIMBING_5p11d 66
#define mCLIMBING_5p12a 69
#define mCLIMBING_5p12b 72
#define mCLIMBING_5p12c 75
#define mCLIMBING_5p12d 78
#define mCLIMBING_5p13a 81
#define mCLIMBING_5p13b 84
#define mCLIMBING_5p13c 87
#define mCLIMBING_5p13d 90
#define mCLIMBING_5p14a 93
#define mCLIMBING_5p14b 96
#define mCLIMBING_5p14c 99

#define mCLIMBING_V0 mCLIMBING_5p5
#define mCLIMBING_V0p mCLIMBING_5p6
#define mCLIMBING_V1 mCLIMBING_5p8
#define mCLIMBING_V2 mCLIMBING_5p9
#define mCLIMBING_V3 mCLIMBING_5p10a
#define mCLIMBING_V4 mCLIMBING_5p10d
#define mCLIMBING_V5 mCLIMBING_5p11b
#define mCLIMBING_V6 mCLIMBING_5p11d
#define mCLIMBING_V7 mCLIMBING_5p12a
#define mCLIMBING_V8 mCLIMBING_5p12c

#define mCLIMBING_SPOT1 mCLIMBING_V0
#define mCLIMBING_SPOT1p mCLIMBING_V1
#define mCLIMBING_SPOT2 mCLIMBING_V1
#define mCLIMBING_SPOT2p mCLIMBING_V2
#define mCLIMBING_SPOT3m mCLIMBING_V2
#define mCLIMBING_SPOT3 mCLIMBING_V3
#define mCLIMBING_SPOT3p mCLIMBING_V4
#define mCLIMBING_SPOT4m mCLIMBING_V5
#define mCLIMBING_SPOT4 mCLIMBING_V6
#define mCLIMBING_SPOT4p mCLIMBING_V7
#define mCLIMBING_SPOT5m mCLIMBING_V7
#define mCLIMBING_SPOT5 mCLIMBING_V8
#define mCLIMBING_SPOT5p mCLIMBING_V9

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
    (1,  'Back Squat'          , 1.45    , "kg"  , "Strength, Squat"),
    (2,  'Bench Press'         , 1.0     , "kg"  , "Strength"),
    (3,  'Climbing'            , 45.0    , "V"   , "Climbing"),
    (4,  'Clean and Jerk'      , 1.0     , "kg"  , "Olympic, Clean"),
    (5,  'Clean'               , 1.0666  , "kg"  , "Olympic, Clean"),
    (6,  'Clean High Pull'     , 1.3     , "kg"  , "Pull"),
    (7,  'Clean Pull'          , 1.3     , "kg"  , "Pull"),
    (8,  'Clean from Knees'    , 0.95    , "kg"  , "Olympic, Clean"),
    (9,  'Crunches'            , 100.0   , "reps", "Core"), 
    (10, 'Curls'               , 0.5     , "kg"  , "Strength"),  
	(11, 'Deadlift'            , 1.8     , "kg"  , "Strength"),
    (12, 'Front Squat'         , 1.224   , "kg"  , "Strength, Squat"),	
    (13, 'Jerk Behink Neck'    , 1.00    , "kg"  , "Olympic, Jerk"), 
    (14, 'Jerk Recover'        , 1.20    , "kg"  , "Olympic, Jerk-Stability"), 
    (15, 'Jerk Rack'           , 1.10    , "kg"  , "Olympic, Jerk"),
    (16, 'Manual Situps'       , 10.0    , "reps", "Core, Partner"),
    (17, 'Overhead Squat'      , 0.88    , "kg"  , "Olympic, Strength, Squat"), 
    (18, 'Plank'               , 120.0   , "sec" , "Core"),
    (19, 'Press'               , 0.75    , "kg"  , "Strength, Press"),
    (20, 'Press Behind Neck'   , 0.825   , "kg"  , "Strength, Press"),
    (21, 'Power Clean'         , 0.825   , "kg"  , "Clean, Olympic"),
    (22, 'Power Snatch'        , 0.66    , "kg"  , "Snatch, Olympic"),
    (23, 'Pull ups'            , 10.0    , "reps", "Core, Strength"),
    (24, 'Push Jerk'           , 1.0     , "kg"  , "Olympic, Jerk"),
    (25, 'Push Press'          , 0.825   , "kg"  , "Strength, Press"),
    (26, 'Push ups'            , 50.0    , "reps", "Strength, Core"),
    (27, 'Sit-ups'             , 100.0   , "reps", "Core"),
    (28, 'Snatch'              , 0.8     , "kg"  , "Olympic, Snatch"),
    (29, 'Snatch Drop'         , 0.85    , "kg"  , "Olympic, Snatch"),
    (30, 'Weighted Vest Plank' , 0.18    , "kg"  , "Core"),

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
