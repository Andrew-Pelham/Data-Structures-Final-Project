#!/usr/bin/env python3

#Imports

import sys
#import pandas as pd
#from datetime import datetime
#import matplotlib.pyplot as plt

#Constants



#Functions

def buildData():
	'''Build dataset from csv file, return to main'''



def buildGraphs(data, day, year, weather, covid):
	'''Select which graphs to display using given flags and call respective functions'''



#Main

def main():
	'''parse flags, and print appropriate data requested'''

#	dict data = buildData()

	flags = sys.argv[1:]
	day = False
	year = False
	weather = False
	covid = False
	

	while len(flags):
		flag = flags.pop(0)
		if flag == '-d':
			day = True
		if flag == '-y':
			year = True
		if flag == '-w':
			weather = True
		if flag == '-c':
			covid = True

	buildGraphs(None, day, year, weather, covid)

if __name__ == '__main__':
	    main()
