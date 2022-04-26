#!/usr/bin/env python3

#Imports

import sys
from datetime import datetime

#Constants



#Functions



#Main

def main():
	'''parse flags, and print appropriate data requested'''

	flags = sys.argv[1:]

	date = #enter day of week
	weather = False

	while len(flags):
		flag = flags.pop(0)
		if flag == '-d':
			date = flags.pop(0)
		if flag == '-w':
			weather = True
