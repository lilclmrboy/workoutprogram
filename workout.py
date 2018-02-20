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

def climbing_convert_range_to_grade(value):

	vgrade = "V0"
	yosgrade = "5.0"
	spotgrade = "1 spot"
	
	if ((value > 0) and (value <= 9)):
		yosgrade = "5.2"
	if ((value > 9) and (value <= 12)):
		yosgrade = "5.3"
	if ((value > 12) and (value <= 15)):
		yosgrade = "5.4"
	if ((value > 15) and (value <= 18)):
		yosgrade = "5.5"
	if ((value > 18) and (value <= 21)):
		yosgrade = "5.6"		
	if ((value > 21) and (value <= 24)):
		yosgrade = "5.7"	
	if ((value > 24) and (value <= 27)):
		yosgrade = "5.8-"
	if ((value > 27) and (value <= 30)):
		yosgrade = "5.8"
	if ((value > 30) and (value <= 33)):
		yosgrade = "5.8+"
	if ((value > 33) and (value <= 36)):
		yosgrade = "5.9-"
	if ((value > 36) and (value <= 39)):
		yosgrade = "5.9"
	if ((value > 39) and (value <= 42)):
		yosgrade = "5.9+"
	if ((value > 42) and (value <= 45)):
		yosgrade = "5.10a"
		vgrade = "V0+"
	if ((value > 45) and (value <= 48)):
		yosgrade = "5.10b"
		vgrade = "V0+"
	if ((value > 48) and (value <= 51)):
		yosgrade = "5.10c"
		vgrade = "V1"
		spotgrade = "2 spot"
	if ((value > 51) and (value <= 54)):
		yosgrade = "5.10d"
		vgrade = "V1"
		spotgrade = "2+ spot"		
	if ((value > 54) and (value <= 57)):
		yosgrade = "5.11a"
		vgrade = "V2"
		spotgrade = "3- spot"
	if ((value > 57) and (value <= 60)):
		yosgrade = "5.11b"
		vgrade = "V3"
		spotgrade = "3 spot"
	if ((value > 60) and (value <= 63)):
		yosgrade = "5.11c"
		vgrade = "V4"
		spotgrade = "3+ spot"
	if ((value > 63) and (value <= 66)):
		yosgrade = "5.11d"
		vgrade = "V4"
		spotgrade = "3+ spot"
	if ((value > 66) and (value <= 69)):
		yosgrade = "5.12a"
		vgrade = "V4"
		spotgrade = "4- spot"
	if ((value > 69) and (value <= 72)):
		yosgrade = "5.12b"
		vgrade = "V5"
		spotgrade = "4- spot"
	if ((value > 72) and (value <= 75)):
		yosgrade = "5.12c"
		vgrade = "V6"
		spotgrade = "4 spot"
	if ((value > 75) and (value <= 78)):
		yosgrade = "5.12d"
		vgrade = "V6"
		spotgrade = "4+ spot"
																															
	return {'yos':yosgrade, 'v':vgrade, 'spot':spotgrade }
		

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
		
		if (units == "yos"):
			if not userPR:
				weight = cnjratio * self.workout_percentOfMax
			else:
				weight = userPR['PR'] * self.workout_percentOfMax
		
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
		
		if (units == "yos"):
			if not userPR:
				weight = cnjratio * self.workout_percentOfMax
			else:
				weight = userPR['PR'] * self.workout_percentOfMax

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
		maxRep = 8
		minRep = 1
		


		# Derive target weights for each sets
		# while at it, find the highest rep count
		# specified in all exercise sets.
		endWeight = exercise.exercise_sets[-1].weight

		for i in range(0, nSets):
			exercise.exercise_sets[i].weight = round((minWeightPercent + i * ((maxWeightPercent - minWeightPercent) / (nSets - 1))) * endWeight)
			if (exercise.exercise_sets[i].repititions > maxRep):
				maxRep = exercise.exercise_sets[i].repititions
				
			if (maxRep > 8):
				maxRep = 8
				
			if (volume < 2000):
				maxRep = 6
				minRep = 3				
				
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
		
	def create_icalendar_workout(self, descName = "workout"):
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
					if (s.units == "yos"):
						climbing = climbing_convert_range_to_grade(s.weight)
						info += "    %s (%s) [%s]\n" % (climbing['yos'], climbing['v'], climbing['spot'])		
					
			event['DESCRIPTION'] = descriptionText
			cal.add_component(event)
				
		# Write the calendar file
		ifilename = "%s-%s.ics" % (descName, self.workoutprogram_username)
		f = open(ifilename, 'wb')
		f.write(cal.to_ical())
		f.close()
		
	######################################################################################

	def create_txt_workout(self, descName = "workout"):
	
		info = "";
	
		for p in self.workoutprogram_workouts:
			info += p.workout_name
			info += '  Targeting %.0f%% of max\n' % (p.workout_percentOfMax * 100.0)
			print info
			for x in p.workout_exercises:
				info += '  %s\n' % x.exercise_name
				set_volume = 0
				for s in x.exercise_sets:
					set_volume = set_volume + s.repititions * s.weight
					if (s.units == "kg"):
						info += "    %d reps x %.0f kg [%.0f lbs]\n" % (s.repititions, s.weight, s.weight * 2.204)
					if (s.units == "reps"):
						info += "    %d reps\n" % s.repititions
					if (s.units == "sec"):
						info += "    %d seconds\n" % s.weight
					if (s.units == "yos"):
						climbing = climbing_convert_range_to_grade(s.weight)
						info += "    x%d %s (%s) [%s]\n" % (s.repititions, climbing['yos'], climbing['v'], climbing['spot'])
									
		ifilename = "%s-%s.txt" % (descName, self.workoutprogram_username)
		f = open(ifilename, 'wb')
		f.write(info)
		f.close()			
		
		
	######################################################################################

	def add_workout(self, i):
		self.workoutprogram_workouts.append(i)
		self.workoutprogram_nWorkoutDays = self.workoutprogram_nWorkoutDays + 1
