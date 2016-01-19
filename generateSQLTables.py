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
    (1, 'Clean and Jerk', 1.0),
    (2, 'Snatch', 0.8),
    (3, 'Bench Press', 1.0),
    (4, 'Clean', 1.0666),
    (5, 'Clean High Pull', 1.3),
    (6, 'Clean Pull', 1.3),
    (7, 'Clean from Knees', 0.95)
)

con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS Exercises")
    cur.execute("CREATE TABLE Exercises(Id INT, Name TEXT, PercentOfCleanAndJerk REAL)")
    cur.executemany("INSERT INTO Exercises VALUES(?, ?, ?)", activities)