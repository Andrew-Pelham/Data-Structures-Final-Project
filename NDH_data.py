import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date




# GATHERING AND SORTING OUT THE CSV DATA

# grab the csv file: This will change depending on the computer
#file_name = '/Users/jamesgalante/Documents/College/Classes/Junior Spring/Data Structures/Project Data/Dining Hall Swipes.csv'
file_name = 'wxswipes.csv'
data = pd.read_csv(file_name)

# Isolate the NDH and NDHGNG data from all the data 
NDH_data = data[data['Group'] == 'NDH'].reset_index(drop=True)
NDHGNG_data = data[data['Group'] == 'NDHGNG'].reset_index(drop=True)

# Convert the dates to a readable format and sort based on date
NDH_data['BUSINESSDATE'] = pd.to_datetime(NDH_data['BUSINESSDATE'], infer_datetime_format=True)
NDHGNG_data['BUSINESSDATE'] = pd.to_datetime(NDHGNG_data['BUSINESSDATE'], infer_datetime_format=True)

NDH_data = NDH_data.sort_values(by='BUSINESSDATE').reset_index(drop=True)
NDHGNG_data = NDHGNG_data.sort_values(by='BUSINESSDATE').reset_index(drop=True)

# Create a Weekday column Mon(0) - Sun(6)
NDH_data['Weekday'] = NDH_data.apply(lambda row: datetime.weekday(row['BUSINESSDATE']), axis=1)
NDHGNG_data['Weekday'] = NDHGNG_data.apply(lambda row: datetime.weekday(row['BUSINESSDATE']), axis=1)

Covid_NDH_data = NDH_data.loc[(pd.to_datetime(NDH_data['BUSINESSDATE']).dt.date > date(2020, 8, 8)) 
	& (pd.to_datetime(NDH_data['BUSINESSDATE']).dt.date < date(2021, 5, 13))]




# These are the hours that the NDH and NDHGNG are open respectively
NDH_dayparts = [7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20]
NDHGNG_dayparts = [10, 11, 12, 13, 14, 15, 16]
# These are the colors of the day of the week along with their names
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdayABREV = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
weather_conditions = ['Snow, Rain, Freezing Drizzle/Freezing Rain, Overcast', 'Rain, Overcast', 
					'Snow, Rain, Partially cloudy', 'Snow, Rain, Ice, Overcast', 
					'Snow, Freezing Drizzle/Freezing Rain, Ice, Partially cloudy', 'Overcast', 
					'Rain, Partially cloudy', 'Clear', 'Snow, Rain, Overcast', 'Partially cloudy', 
					'Snow, Ice, Partially cloudy', 'Rain', 'Snow, Partially cloudy', 'Snow, Overcast']




# Average Swipes per Time of Day: Note that the hours chosen are the hours that each is open
def AllAvgSwipesTOD(NDH_data, NDHGNG_data, NDH_dayparts, NDHGNG_dayparts):
	NDHGNG_daypart_means = []
	NDH_daypart_means = []

	# Collecting NDH and NDHGNG mean per daypart data
	for daypart in NDH_dayparts: 
		mean = NDH_data.loc[NDH_data['DAYPART'] == daypart, 'Swipes'].mean()
		NDH_daypart_means.append(mean)

	for daypart in NDHGNG_dayparts:
		mean = NDHGNG_data.loc[NDHGNG_data['DAYPART'] == daypart, 'Swipes'].mean()
		NDHGNG_daypart_means.append(mean)


	# Create two plots and add the bar graphs
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
	axes[0].bar(NDH_dayparts, NDH_daypart_means)
	axes[1].bar(NDHGNG_dayparts, NDHGNG_daypart_means, color='r')

	# Set the axes labels and the titles
	axes[0].set_xlabel("Time of Day (Military Time)")
	axes[1].set_xlabel("Time of Day (Military Time)")
	axes[0].set_ylabel("Average Swipes")
	axes[0].set_title("Average Swipes per Time of Day at NDH")
	axes[1].set_title("Average Swipes per Time of Day at NDHGNG")

	# Tighten up the layout and print the output
	fig.tight_layout()
	plt.show()

# Average Swipes for day of week: Purely relational as it doesn't discriminate between semester
def AveragePerDOW(NDH_data, NDH_dayparts, weekday):
	weekday_means = []

	# For each weekday get the necessary data
	for i in range(7):
		mean = NDH_data.loc[(NDH_data['Weekday'] == i) & (NDH_data['DAYPART'].isin(NDH_dayparts)), 'Swipes'].mean()
		weekday_means.append(mean)

	# Format the output table
	plt.title("Averages Swipes per Day of Week")
	plt.xlabel("Day of the Week")
	plt.ylabel("Average Swipes")
	plt.bar(weekday, weekday_means)
	plt.show()

# Total Swipes for each day displayed as a scatter plot
def TotalSwipesScatter(NDH_data, NDH_dayparts, weekday, axes=None, col=None, Colors=True, Show=True, Title=None):
	# Returns a list of all the dates sorted
	dates = set()
	for idx, row in NDH_data.iterrows():
		dates.add(row['BUSINESSDATE'])	
	dates = list(dates)
	dates.sort()


	# Return the total amount of swipes for each date
	sum_dates = []
	for date in dates:
		sum_date = NDH_data.loc[(NDH_data['BUSINESSDATE'] == date) & (NDH_data['DAYPART'].isin(NDH_dayparts)), 'Swipes'].sum()
		sum_dates.append(sum_date)


	# Create a dataframe of the dates, sum_dates, and weekdays for each date
	datesdict = {'Dates': dates, 'Sums': sum_dates}
	df = pd.DataFrame(datesdict)
	df['Weekday'] = df.apply(lambda row: datetime.weekday(row['Dates']), axis=1)


	# Plot each date and it's total amt of swipes. Also, label the date according to its weekday
	plt.figure(figsize=(8, 5))
	if (Colors):
		plt.title(Title)
		plt.ylabel("Total Swipes")
		plt.xlabel("Date")
		for i in range(7):
			plt.scatter(df.loc[df['Weekday'] == i, 'Dates'], df.loc[df['Weekday'] == i, 'Sums'], label=weekday[i], s=10)
		plt.legend(loc=2, ncol=len(df.columns))
	else:
		color = 'red'
		if (col == 0):
			color = 'blue'
		axes[col].scatter(df['Dates'], df['Sums'], s=10, color=color)

	if (Show):
		plt.show()

# Average Swipes per Time of Day for each Day of the week
def AvgSwipesPerTimeDOW(NDH_data, NDH_dayparts, axes, DOW, colors, weekday):
	NDH_daypart_means = []

	# Collecting NDH and NDHGNG mean per daypart data
	for daypart in NDH_dayparts: 
		mean = NDH_data.loc[(NDH_data['DAYPART'] == daypart) & (NDH_data['Weekday'] == DOW), 'Swipes'].mean()
		NDH_daypart_means.append(mean)

	# Making sure that the week days are in the correct subplots
	row = 0
	if (DOW > 3):
		row = 1

	# Plotting the weekdays and giving the correct labels
	axes[row, DOW % 4].set_ylabel("Average Swipes")
	axes[row, DOW % 4].set_xlabel("Time of Day")
	axes[row, DOW % 4].bar(NDH_dayparts, NDH_daypart_means, color=colors[DOW])
	axes[row, DOW % 4].set_ylim(top = 800)
	axes[row, DOW % 4].set_title(weekday[DOW])

# Plotting function for AvgSwipesPerTimeDOW
def AllAvgDOW():
	#Create a subplot for each weekday
	fig, DOW_axes = plt.subplots(nrows=2, ncols=4, figsize=(15, 7.5))

	# Run through the Avg SqipesPerTimeDOW function for each DOW
	for i in range(7):
		AvgSwipesPerTimeDOW(NDH_data, NDH_dayparts, DOW_axes, i, colors, weekday)

	# Format and show the plot
	fig.tight_layout()
	plt.show()

#Plotting function for the NDH and GNG Scatterplots
def NDH_and_GNG_Scatters():

	# Create a subplot for both types of data
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 4))

	axes[0].set_title("NDH data")
	axes[1].set_title("GNG data")
	axes[0].set_xlabel("Date")
	axes[1].set_xlabel("Date")
	axes[0].set_ylabel("Total Swipes")
	# Run both scatterplots
	TotalSwipesScatter(NDH_data, NDH_dayparts, weekdayABREV, axes, 0, Colors=False, Show=False)
	TotalSwipesScatter(NDHGNG_data, NDHGNG_dayparts, weekdayABREV, axes, 1, Colors=False, Show=False)

	# Format plotting
	fig.tight_layout()
	plt.show()

# Frequency of Swipes per Weather Condition
def SwipesPerWeather(weather_conditions, NDH_Data, NDH_dayparts):

	condition_means = []

	# Get the lengths to split up the weather conditions because they won't all fit on one line
	mid = int(len(weather_conditions) / 3)
	mid2 = int(2*mid)

	fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 6))

	# The next three sections get the relevant data and add that data to the subplots
	for condition in weather_conditions[:mid]:
		mean = NDH_data.loc[(NDH_data['Condition'] == condition) & NDH_data['DAYPART'].isin(NDH_dayparts), 'Swipes'].mean()
		condition_means.append(mean)
	axes[0].bar(weather_conditions[:mid], condition_means)
	axes[0].set_ylim(top=450)

	condition_means = []

	for condition in weather_conditions[mid:mid2 + 1]:
		mean = NDH_data.loc[(NDH_data['Condition'] == condition) & NDH_data['DAYPART'].isin(NDH_dayparts), 'Swipes'].mean()
		condition_means.append(mean)
	axes[1].bar(weather_conditions[mid:mid2 + 1], condition_means)
	axes[1].set_ylim(top=450)

	condition_means = []

	for condition in weather_conditions[mid2 + 1:]:
		mean = NDH_data.loc[(NDH_data['Condition'] == condition) & NDH_data['DAYPART'].isin(NDH_dayparts), 'Swipes'].mean()
		condition_means.append(mean)
	axes[2].bar(weather_conditions[mid2 + 1:], condition_means)
	axes[2].set_ylim(top=450)

	# Set the rotation of all of the xlabels
	#axes[0].set_xticklabels(weather_conditions[:mid], rotation=5)
	#axes[1].set_xticklabels(weather_conditions[mid:mid2], rotation=5)
	#axes[2].set_xticklabels(weather_conditions[mid2:], rotation=5)

	# Set all the ylabels
	axes[0].set_ylabel("Average Swipes")
	axes[1].set_ylabel("Average Swipes")
	axes[2].set_ylabel("Average Swipes")

	# Format the final plot
	fig.suptitle("Average Swipes for each Weather Condition")
	fig.tight_layout()
	plt.show()
	


# Executing all of the functions
AllAvgSwipesTOD(NDH_data, NDHGNG_data, NDH_dayparts, NDHGNG_dayparts)
AveragePerDOW(NDH_data, NDH_dayparts, weekdayABREV)
AllAvgDOW()
TotalSwipesScatter(NDH_data, NDH_dayparts, weekdayABREV, Colors=True, Show=True, Title="NDH_data")
TotalSwipesScatter(NDHGNG_data, NDHGNG_dayparts, weekdayABREV, Colors=True, Show=True, Title="GNG Data")
NDH_and_GNG_Scatters()
TotalSwipesScatter(Covid_NDH_data, NDH_dayparts, weekdayABREV, Colors=True, Show=True, Title="NDH Covid Semester")
SwipesPerWeather(weather_conditions, NDH_data, NDH_dayparts)


