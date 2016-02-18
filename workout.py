#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import math
import random
import sqlite3 as lite

##########################################################################################

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
##########################################################################################


def periodization_equation(step, nTotalSteps, base = 0.6, nCycles = 3.0):
	percent = 0.0
	offset = 0.5
	xOffset = 6.0
	rate = 0.3
	x = step
	a = float(nTotalSteps) / float(nCycles)
	z = (x + xOffset) / a
	
	period = offset + z - math.floor(z + 0.5)
	percent = ((rate / nTotalSteps) * x + base) + 0.1 * period

	return percent    

##########################################################################################

def Error(current, desired, errorResult):

	error = 0.0
	errorOld = errorResult
	bSmallerError = 0

	error = math.fabs((desired - current) / desired)

	if (error < errorOld):
		bSmallerError = 1
		errorResult = error

	return {'isLower':bSmallerError, 'error':errorResult}

##########################################################################################

class ExerciseDetail(object):

	def __init__(self, weight, repititions = 1, time = 0.0):
		self.repititions = repititions
		self.weight = weight
		self.time = time

##########################################################################################

class Exercise(object):

	def __init__(self, name):
		self.exercise_name = name
		self.exercise_sets = []
		# self.exercise_volume = 0

	def add_set(self, weight, repititions = 1, time = 0.0):
		self.exercise_sets.append(ExerciseDetail(weight, repititions, time))

##########################################################################################

class Workout(object):

	def __init__(self, name, dt, pmax, volume, cnj = 100.0):
		self.workout_name = name
		self.workout_dt = dt
		self.workout_exercises = []
		self.workout_percentOfMax = pmax
		self.workout_volume = volume
		self.workout_cnj_max = cnj
		self.workout_database = "test.db"
		
	######################################################################################

	def pick_random_exercise(self, exStyle):
		con = lite.connect(self.workout_database)
		con.row_factory = lite.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM Exercises WHERE Type like '%{tn}%'".format(tn=exStyle))
		rows = cur.fetchall()
		# for row in rows:
		# 	print("Found exercise that matches type %s: %s" % (type, row["Name"]))
		con.close()
		exResult = random.choice(rows)
		return {'name':str(exResult["Name"])}


	######################################################################################

	def add_exercise(self, ex):
		self.workout_exercises.append(ex)

	######################################################################################

	def add_exercise_target_volume(self, exname, nsets, nrepsmax = 8, minRep = 1):
		print "begin adding exercise target volume"
		
		con = lite.connect(self.workout_database)
		con.row_factory = dict_factory
		cur = con.cursor()
		cur.execute("SELECT Name, PercentOfCleanAndJerk FROM Exercises WHERE Name is '{tn}'".format(tn=exname))
		result = cur.fetchone()
		con.close()
		
		ex = Exercise(result['Name'])
		cnjratio = result['PercentOfCleanAndJerk']
				
		for i in range(0, nsets):
			ex.add_set(cnjratio * self.workout_cnj_max, nrepsmax)
		self.add_exercise(ex)
		
		print self.workout_volume
		
		result = self.solve_exercise_volume(self.workout_exercises[-1], self.workout_volume)

	######################################################################################

	def solve_exercise_volume(self, exercise, volume, minWeightPercent = 0.7, maxWeightPercent = 1.0, minSets = 1, maxSets = 10):

		error = 1.0e9
		xLimitMax = 1000
		nSets = len(exercise.exercise_sets)
		ModeType = 1
		volume_best = 0
		maxRep = 1
		minRep = 1

		# Derive target weights for each sets
		# while at it, find the highest rep count
		# specified in all exercise sets.
		endWeight = exercise.exercise_sets[-1].weight

		for i in range(0, nSets):
			exercise.exercise_sets[i].weight = round((minWeightPercent + i * ((maxWeightPercent - minWeightPercent) / (nSets - 1))) * endWeight)
			if (exercise.exercise_sets[i].repititions > maxRep):
				maxRep = exercise.exercise_sets[i].repititions

		if (minRep != 1):
			for i in range(0, nSets):
				if (exercise.exercise_sets[i].repititions < minRep):
					minRep = exercise.exercise_sets[i].repititions

		# print("- Solving exercise %s for volume of %.1f kg" % (exercise.exercise_name, volume))
		# print("  Minimum reps: %d Maximum reps: %d" % (minRep, maxRep))
		# print("  Setting %% range from %.2f to %.2f" % (minWeightPercent, maxWeightPercent))
		# print("  Targeting %d sets for target volume of %.1f" % (nSets, volume))

		for x in range(0, xLimitMax):

			setReps_calc = []
			volume_calc = 0

			for i in range(0, nSets):
				setReps_calc.append(random.randint(minRep, maxRep))
				volume_calc = volume_calc + exercise.exercise_sets[i].weight * setReps_calc[i]
				# print("volume_calc: %f" % volume_calc)

			# Get the absolute error value
			error_total = math.fabs(volume - volume_calc)

			errorResult = Error(error_total, 0.000001, error)
			error = errorResult['error']

			if (errorResult['isLower']):
				# print volume_calc
				self.workout_volume = volume_calc
				volume_best = volume_calc
				# print volume_best
				for i in range(0, nSets):
					exercise.exercise_sets[i].repititions = setReps_calc[i]

		return {'volume': volume_best}

##########################################################################################

class WorkoutProgram(object):

	def __init__(self, description, dt, volume, nweeks, username, cnj = 100.0):
		self.workoutprogram_description = description
		self.workoutprogram_dt_start = dt
		self.workoutprogram_volume_max = volume
		self.workoutprogram_cnj_max = cnj
		self.workoutprogram_username = username
		self.workoutprogram_workouts = []
		self.workoutprogram_nWeeks = nweeks
		self.workoutprogram_nWorkoutsPerWeek = 3
		self.workoutprogram_nWorkoutDays = 0

	######################################################################################

	def add_workout(self, i):
		self.workoutprogram_workouts.append(i)
		self.workoutprogram_nWorkoutDays = self.workoutprogram_nWorkoutDays + 1
