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
import argparse


###################################################################################################
###################################################################################################

def main(argv):
    parser = argparse.ArgumentParser(description='Generate Automation Scripts for PBULD00171 development.')
    parser.add_argument('--weeks', help='Number of weeks for workout', type=int, default=12)
    parser.add_argument('--user', help='Username for workout', default='Matt')
    parser.add_argument('--volume', help='Volume for workout to targer', type=float, default=2000.0)
    dv = parser.parse_args(argv)

    # where:
    # 0 - Sunday
    # 1 - Monday
    # 2 - Tuesday
    # 3 - Wednesday
    # 4 - Thursday
    # 5 - Friday
    # 6 - Saturday

    print ("Generating workout program")

    startdate = datetime(2017, 7, 10, tzinfo=pytz.utc)
    volume = dv.volume
    workout_day_inc = [1, 2, 2, 2]
    wp = WorkoutProgram("Strength Training", startdate, volume, dv.weeks, dv.user)
    dayIndex = 0
    workoutCount = 0
    totalWorkouts = (len(workout_day_inc) - 1) * dv.weeks

    # ------------------ Workout Generation --------------------#
    for week in range(0, wp.workoutprogram_nWeeks):
        dayIndex = dayIndex + workout_day_inc[0]
        wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
        workoutCount = workoutCount + 1
        workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
        wkout = Workout(dv.user, "%s - Strength" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
        rndex = wkout.pick_random_exercise("Press")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        rndex = wkout.pick_random_exercise("Jerk")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        rndex = wkout.pick_random_exercise("Squat")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        wkout.add_exercise_target_volume("Deadlift", 5)
        wkout.add_exercise("Push ups")
        rndex = wkout.pick_random_exercise("Core")
        wkout.add_exercise(rndex['name'])
        wp.add_workout(wkout)

        wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
        workoutCount = workoutCount + 1
        dayIndex = dayIndex + workout_day_inc[1]
        workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
        wkout = Workout(dv.user, "%s - Strength" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
        rndex = wkout.pick_random_exercise("Press")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        rndex = wkout.pick_random_exercise("Clean")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        rndex = wkout.pick_random_exercise("Squat")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        wkout.add_exercise_target_volume("Deadlift", 5)
        wkout.add_exercise("Push ups")
        rndex = wkout.pick_random_exercise("Core")
        wkout.add_exercise(rndex['name'])
        wp.add_workout(wkout)

        wPercent = workout.periodization_equation(workoutCount, totalWorkouts)
        workoutCount = workoutCount + 1
        dayIndex = dayIndex + workout_day_inc[2]
        workoutdate = wp.workoutprogram_dt_start + timedelta(days=dayIndex)
        wkout = Workout(dv.user, "%s - Olympic" % (workoutdate.strftime("%A")), workoutdate, wPercent, volume)
        rndex = wkout.pick_random_exercise("Press")
        wkout.add_exercise_target_volume(rndex['name'], 5)
        wkout.add_exercise_target_volume("Clean and Jerk", 8)
        wkout.add_exercise_target_volume("Deadlift", 5)
        wkout.add_exercise("Pull ups")
        rndex = wkout.pick_random_exercise("Core")
        wkout.add_exercise(rndex['name'])

        wp.add_workout(wkout)
        dayIndex = dayIndex + workout_day_inc[3]

    wp.create_txt_workout()
    wp.create_icalendar_workout()


###################################################################################################
###################################################################################################
###################################################################################################

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
