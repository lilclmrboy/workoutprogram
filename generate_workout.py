#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import sys
from workout import ExerciseDetail
from workout import Exercise
from workout import Workout
from workout import WorkoutProgram
from datetime import datetime, timedelta
from pytz import timezone
import pytz

# where:
# 0 - Sunday
# 1 - Monday
# 2 - Tuesday
# 3 - Wednesday
# 4 - Thursday
# 5 - Friday
# 6 - Saturday
workout_day_intervals = [1, 3, 5]

print ("Generating workout program")

startdate = datetime(2016,2,14,tzinfo=pytz.utc)
volume = 1000.0
wp = WorkoutProgram("Strength Training", startdate, volume, 2, "matt")

print startdate.strftime("%A")

newdt = startdate + timedelta(days=3)
print newdt.strftime("%A")

for week in range(0, wp.workoutprogram_nWeeks):
    workoutdate = wp.workoutprogram_dt_start + timedelta(days=1)
    wkout = Workout("%s - Strength" % workoutdate.strftime("%A"), workoutdate, 0.6, volume)

wkout = Workout("Workout description", startdate, 0.6, volume)
wkout.add_exercise_target_volume("Press", 100.0, 6)
wkout.add_exercise_target_volume("Squat", 100.0, 3)

# print wkout.exercises[0].name
print wkout.workout_name
print('Workout %% of max: %.2f' % wkout.workout_percentOfMax)
for x in wkout.workout_exercises:
    print('Exercise name: %s' % x.exercise_name)
    #wkout.solve_activity_volume(x, volume)
    print(' Derived volume: %.2f kg' % wkout.workout_volume)
    for s in x.exercise_sets:
        print("  Set %d reps x %.0f kg" % (s.repititions, s.weight))
