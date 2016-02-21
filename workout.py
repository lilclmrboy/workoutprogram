#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import math
import random
from datetime import datetime, timedelta
from dateutil import tz
import sqlite3 as lite
from icalendar import Calendar, Event
import tempfile, os

##########################################################################################

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
##########################################################################################


def periodization_equation(step, nTotalSteps, base = 0.6, nCycles = 3.0):
	percent = 0.0
 	rate = 0.3
 	x = step

	maxSteps = float(nTotalSteps) - 1.0

	b = ((float(maxSteps) + 1)/ nCycles)
 	period = (math.fmod(step, b) * b / (b - 1.0)) / b
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

	def __init__(self, weight, repititions = 1, time = 0.0, units = ""):
		self.repititions = repititions
		self.weight = weight
		self.time = time
		self.units = units

##########################################################################################

class Exercise(object):

	def __init__(self, name, bOptional = 0):
		self.exercise_name = name
		self.exercise_sets = []
		# self.exercise_volume = 0
		self.exercise_isoptional = bOptional
		self.exercise_units = ""

	def add_set(self, weight, repititions = 1, time = 0.0, units = ""):
		self.exercise_units = units
		self.exercise_sets.append(ExerciseDetail(weight, repititions, time, units))

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
 		return {'name':str(exResult['Name'])}

	######################################################################################

	def add_exercise(self, exname, nSets = 1, minWeightPercent = 0.7, maxWeightPercent = 1.0, bOptional = 0):
		con = lite.connect(self.workout_database)
		con.row_factory = dict_factory
		cur = con.cursor()
		cur.execute("SELECT PercentOfCleanAndJerk, Units FROM Exercises WHERE Name is '{tn}'".format(tn=exname))
		result = cur.fetchone()
		cur.execute("SELECT * FROM UserRecords WHERE Exercise is '{tn}'".format(tn=exname))
		userPR = cur.fetchone()
		con.close()
		
		cnjratio = result['PercentOfCleanAndJerk']
		units = result['Units']
		time = 0.0
		reps = 1.0
		
		ex = Exercise(exname)
		
		if (units == "reps"):
			reps = cnjratio * self.workout_percentOfMax
			ex.add_set(1.0, reps, time, units)
			
		if (units == "kg"):
			weight = 0.0
			if not userPR:
				weight = cnjratio * self.workout_percentOfMax * self.workout_cnj_max
			else:
# 				print "PR defined for %s" % userPR['Exercise']
				weight = userPR['PR'] * self.workout_percentOfMax
			
			for i in range(0, nSets):
				ex.add_set(weight, reps, time, units)
						    
 		self.workout_exercises.append(ex)

	######################################################################################

	def add_exercise_target_volume(self, exname, nsets, nrepsmax = 8, minRep = 1, bOptional = 0):
# 		print "begin adding exercise target volume"
		
		con = lite.connect(self.workout_database)
		con.row_factory = dict_factory
		cur = con.cursor()
		cur.execute("SELECT Name, PercentOfCleanAndJerk, Units FROM Exercises WHERE Name is '{tn}'".format(tn=exname))
		result = cur.fetchone()
		cur.execute("SELECT * FROM UserRecords WHERE Exercise is '{tn}'".format(tn=exname))
		userPR = cur.fetchone()
		con.close()
		
		ex = Exercise(result['Name'], bOptional)
		cnjratio = result['PercentOfCleanAndJerk']
		units = result['Units']
		time = 0.0
		weight = 0.0

		if (units == "kg"):
			if not userPR:
				weight = cnjratio * self.workout_percentOfMax * self.workout_cnj_max
			else:
# 				print "PR defined for %s" % userPR['Exercise']
				weight = userPR['PR'] * self.workout_percentOfMax
		
		# Decrease our maximum number of reps as we get closer to our max percent
		# Function  :	Polynomial
		# Descr 1  :	f(x) = const + a1*x +...+ a3*x^3
		# Descr 2  :	deg: degree of the polynomial
		# deg  	=	   3.0000
		const	=	 162.0201   
		a1   	=	-499.2764   
		a2   	=	 540.4491   
		a3   	=	-202.1640   
		x = self.workout_percentOfMax
		if (nrepsmax == 8):
			nrepsmax = int(const + a1 * x + a2 * x * x + a3 * x * x * x)
				
		for i in range(0, nsets):
			ex.add_set(weight, nrepsmax, time, units)
		self.workout_exercises.append(ex)
		
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

	def __init__(self, description, utc, volume, nweeks, username, cnj = 100.0):
		self.workoutprogram_description = description
		
		self.workoutprogram_volume_max = volume
		
		self.workoutprogram_username = username
		self.workoutprogram_workouts = []
		self.workoutprogram_nWeeks = nweeks
		self.workoutprogram_nWorkoutsPerWeek = 3
		self.workoutprogram_nWorkoutDays = 0
		self.workoutprogram_database = "test.db"
		
		con = lite.connect(self.workoutprogram_database)
		con.row_factory = dict_factory
		cur = con.cursor()
		cur.execute("SELECT * FROM UserRecords WHERE FirstName is '{tn}' AND Exercise is '{tx}'".format(tn=self.workoutprogram_username, tx="Clean and Jerk"))
		result = cur.fetchone()
		con.close()
		
		self.workoutprogram_cnj_max = result["PR"]
		
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()
		
		myutc = utc.replace(tzinfo=from_zone)
		self.workoutprogram_dt_start = myutc.astimezone(to_zone)
	
	######################################################################################
		
	def create_icalendar_workout(self):
		print "Generating iCalendar"
		cal = Calendar()
		cal.add('prodid', '-//My workout calendar//mxm.dk//')
		cal.add('version', '2.0')
		
		for p in self.workoutprogram_workouts:
			event = Event()
			event.add('summary', p.workout_name)
			event.add('dtstart', p.workout_dt + timedelta(hours=-11))
			event.add('dtend',   p.workout_dt + timedelta(hours=-9))
			descriptionText = "%.0f%% of max targeting %.f kg volume\n\n" % (100.0 * p.workout_percentOfMax, self.workoutprogram_volume_max)
			
			for x in p.workout_exercises:
				descriptionText += '  %s\n' % x.exercise_name
				for s in x.exercise_sets:
					if (s.units == "kg"):
						descriptionText += "    %d reps x %.0f kg [%.0f lbs]\n" % (s.repititions, s.weight, s.weight * 2.204)
					if (s.units == "reps"):
						descriptionText += "    %d reps\n" % s.repititions
					if (s.units == "sec"):
						descriptionText += "    %d seconds\n" % s.weight
					
			event['DESCRIPTION'] = descriptionText
			cal.add_component(event)
				
		# Write the calendar file
		ifilename = "workout-%s.ics" % self.workoutprogram_username
		f = open(ifilename, 'wb')
		f.write(cal.to_ical())
		f.close()
		
	######################################################################################

	def add_workout(self, i):
		self.workoutprogram_workouts.append(i)
		self.workoutprogram_nWorkoutDays = self.workoutprogram_nWorkoutDays + 1
