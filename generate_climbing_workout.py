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

print ("Generating climbing workout program")

startdate = datetime(2016,2,29,tzinfo=pytz.utc)
volume = 550.0
workout_day_inc = [1, 2, 2, 2]
wp = WorkoutProgram("Climbing Training", startdate, volume, 12, "Matt")
dayIndex = 0
workoutCount = 0
totalWorkouts = 36

# ------------------ Workout Generation --------------------#
for week in range(0, wp.workoutprogram_nWeeks):

	dayIndex = dayIndex + workout_day_inc[0]
	wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
	workoutCount = workoutCount + 1 
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s - Strength" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Climbing", 8)
	rndex = wkout.pick_random_exercise("Core")
 	wkout.add_exercise(rndex['name'])
	wp.add_workout(wkout)
	
	wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
	workoutCount = workoutCount + 1
	dayIndex = dayIndex + workout_day_inc[1]
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s - Strength" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Climbing", 8)
	rndex = wkout.pick_random_exercise("Core")
 	wkout.add_exercise(rndex['name'])
	wp.add_workout(wkout)
	
	wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
	workoutCount = workoutCount + 1
	dayIndex = dayIndex + workout_day_inc[2]
	workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
	wkout = Workout("%s - Olympic" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
	wkout.add_exercise_target_volume("Climbing", 8)
	rndex = wkout.pick_random_exercise("Core")
 	wkout.add_exercise(rndex['name'])
 	
	wp.add_workout(wkout)
	dayIndex = dayIndex + workout_day_inc[3]


wp.create_txt_workout("climbing")
# wp.create_icalendar_workout()

