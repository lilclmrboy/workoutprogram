#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import sys
import workout
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

print ("Generating workout program")

startdate = datetime(2016,2,14,tzinfo=pytz.utc)
volume = 1000.0
workout_day_inc = [1, 2, 2, 2]
wp = WorkoutProgram("Strength Training", startdate, volume, 12, "matt")
dayIndex = 0
workoutCount = 0

# ------------------ Workout Generation --------------------#
for week in range(0, wp.workoutprogram_nWeeks):

	dayIndex = dayIndex + workout_day_inc[0]
	wPercent = workout.periodization_equation(workoutCount, 36)
	workoutCount = workoutCount + 1 
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s %s, %s (%s) - Strength" % (workoutdate.strftime("%B"), workoutdate.strftime("%d"), workoutdate.strftime("%Y"), workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Snatch", 6)
	#     rndex = wkout.pick_random_exercise("Core")
	#     wkout.add_exercise(rndex['name'])
	wp.add_workout(wkout)
	
	wPercent = workout.periodization_equation(workoutCount, 36)
	workoutCount = workoutCount + 1
	dayIndex = dayIndex + workout_day_inc[1]
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s %s, %s (%s) - Strength" % (workoutdate.strftime("%B"), workoutdate.strftime("%d"), workoutdate.strftime("%Y"), workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Clean and Jerk", 6)
	wp.add_workout(wkout)
	
	wPercent = workout.periodization_equation(workoutCount, 36)
	workoutCount = workoutCount + 1
	dayIndex = dayIndex + workout_day_inc[2]
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s %s, %s (%s) - Olympic" % (workoutdate.strftime("%B"), workoutdate.strftime("%d"), workoutdate.strftime("%Y"), workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Snatch", 6)
	wp.add_workout(wkout)
	dayIndex = dayIndex + workout_day_inc[3]

# ----------------- Show the results ------------------------#
# print wkout.exercises[0].name
for p in wp.workoutprogram_workouts:
    print p.workout_name
    print('  Targeting %.0f%% of max' % (p.workout_percentOfMax * 100.0))
#     for x in p.workout_exercises:
#         print('  Exercise name: %s' % x.exercise_name)
#         #wkout.solve_activity_volume(x, volume)
#         print('   Derived volume: %.2f kg' % p.workout_volume)
#         for s in x.exercise_sets:
#             print("  Set %d reps x %.0f kg" % (s.repititions, s.weight))

# ----------------- End show result ------------------------#
