#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import sys
from workout import ExerciseDetail
from workout import Exercise
from workout import Workout
from datetime import datetime
from pytz import timezone
import pytz

print ("Generating workout program")

dt = datetime(2016,4,4,tzinfo=pytz.utc)
print dt
wkout = Workout("Workout description", dt, 0.6)

ex = Exercise("Snatch")
ex.add_set(100.0, 5)
ex.add_set(100.0, 4)
ex.add_set(100.0, 3)
ex.add_set(100.0, 3)
wkout.add_exercise(ex)

ex = Exercise("Squat")
ex.add_set(100.0, 5)
ex.add_set(100.0, 4)
ex.add_set(100.0, 3)
ex.add_set(100.0, 2)
ex.add_set(100.0, 1)
wkout.add_exercise(ex)

print wkout.name
print('Workout %% of max: %.2f' % wkout.percentOfMax)

# print wkout.exercises[0].name
volume = 1000.0

for x in wkout.activities:
    print('Activity name: %s' % x.name)
    wkout.solve_activity_volume(x, volume)
    print(' Derived volume: %.2f kg' % x.volume)
    for s in x.sets:
        print("  Set %d reps x %.2f kg" % (s.repititions, s.weight))




    # print x.sets
    # for s in x.sets:
    #     print("\t%d x X", (s.repititions % s.weight))

# for activities in wkout.exercises
#     print activites.name
    # for e in w.exercises:
    #     print e.name
    #     for s in e.sets:
    #         print s.repitions
