#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python rewrite of:
#   https://code.google.com/p/weightliftingworkout/source/browse/#svn%2Ftrunk%253Fstate%253Dclosed

import math
import random

def Error(current, desired, errorResult):

	error = 0.0
	errorOld = errorResult
	bSmallerError = 0

	error = math.fabs((desired - current) / desired)

	if (error < errorOld):
		bSmallerError = 1
		errorResult = error

	return {'isLower':bSmallerError, 'error':errorResult}

class ExerciseDetail(object):

	def __init__(self, weight, repititions = 1, time = 0.0):
		self.repititions = repititions
		self.weight = weight
		self.time = time

class Exercise(object):

	def __init__(self, name):
		self.name = name
		self.sets = []
		self.volume = 0

	def add_set(self, weight, repititions = 1, time = 0.0):
		self.sets.append(ExerciseDetail(weight, repititions, time))

class Workout(object):

	def __init__(self, name, dt, pmax):
		self.name = name
		self.dt = dt
		self.activities = []
		self.percentOfMax = pmax

	def add_exercise(self, i):
		self.activities.append(i)

	def solve_activity_volume(self, activity, volume, minWeightPercent = 0.7, maxWeightPercent = 1.0, minSets = 1, maxSets = 10):

		error = 1.0e9
		xLimitMax = 100000
		nSets = len(activity.sets)
		ModeType = 1

		# Derive target weights for each sets
		endWeight = activity.sets[0].weight
		maxRep = 1

		for i in range(0, nSets):

			if (activity.sets[i].repititions > maxRep):
				maxRep = activity.sets[i].repititions

		minRep = maxRep

		for i in range(0, nSets):

			if (activity.sets[i].repititions < minRep):
				minRep = activity.sets[i].repititions

			activity.sets[i].weight = round((minWeightPercent + i * ((maxWeightPercent - minWeightPercent) / (nSets - 1))) * endWeight)

		print("- Solving activity %s for volume of %.1f kg" % (activity.name, volume))
		# print("  Minimum reps: %d Maximum reps: %d" % (minRep, maxRep))
		# print("  Setting %% range from %.2f to %.2f" % (minWeightPercent, maxWeightPercent))
		# print("  Targeting %d sets for target volume" % nSets)

		for x in range(0, xLimitMax):

			setReps_calc = []
			volume_calc = 0

			for i in range(0, nSets):
				setReps_calc.append(random.randint(minRep, maxRep))
				volume_calc = volume_calc + activity.sets[i].weight * setReps_calc[i]

			# Get the absolute error value
			error_total = math.fabs(volume - volume_calc)

			errorResult = Error(error_total, 0.000001, error)
			error = errorResult['error']

			if (errorResult['isLower']):
				activity.volume = volume_calc
				for i in range(0, nSets):
					activity.sets[i].repititions = setReps_calc[i]
