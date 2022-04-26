import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# BUSINESSDATE DAYPART FromTo Group Swipes

# grab the csv file
file_name = '/Users/jamesgalante/Documents/College/Classes/Junior Spring/Data Structures/Project Data/Dining Hall Swipes.csv'
data = pd.read_csv(file_name)


# Isolate the NDH data from all the data and drop the Group
NDH_data = data[data['Group'] == 'NDH'].reset_index(drop=True)
del NDH_data['Group']


# Convert the dates to a readable format and sort based on date
NDH_data['BUSINESSDATE'] = pd.to_datetime(NDH_data['BUSINESSDATE'], infer_datetime_format=True)
NDH_data = NDH_data.sort_values(by='BUSINESSDATE').reset_index(drop=True)

# Create a Weekday column Mon(0) - Sun(6)
NDH_data['Weekday'] = NDH_data.apply(lambda row: datetime.weekday(row['BUSINESSDATE']), axis=1)

print(NDH_data)


DAYPART = set()

for idx, row in NDH_data.iterrows():
	DAYPART.add((row['DAYPART'], row['FromTo']))


# all the possible times in order
# Should we take out all not actual hours of the dining hall?
ordered_times = [
#	(0, '12:00am 01:00am'),
#	(2, '02:00am 03:00am')
#	(6, '06:00am 07:00am'), 
	(7, '07:00am 08:00am'),
	(8, '08:00am 09:00am'),
	(9, '09:00am 10:00am'),
	(10, '10:00am 11:00am'),
	(11, '11:00am 12:00pm'),
	(12, '12:00pm 01:00pm'),
	(13, '01:00pm 02:00pm'),
#	(14, '02:00pm 03:00pm'),
#	(15, '03:00pm 04:00pm'),
	(16, '04:00pm 05:00pm'),
	(17, '05:00pm 06:00pm'),
	(18, '06:00pm 07:00pm'),
	(19, '07:00pm 08:00pm'),
	(20, '08:00pm 09:00pm'),
#	(21, '09:00pm 10:00pm'),
#	(22, '10:00pm 11:00pm'),
#	(23, '11:00pm 12:00am'),
]


# Averate Swipes per Time of Day
dayparts = [7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20]
daypart_means = []

for daypart in dayparts: 
	mean = NDH_data.loc[NDH_data['DAYPART'] == daypart, 'Swipes'].mean()
	daypart_means.append(mean)

plt.bar(dayparts, daypart_means)
plt.title("Average Swipes per Time of Day")
plt.xlabel("Time of Day (Military Time)")
plt.ylabel("Average Swipes")
plt.show()


# Average Swipes for day of week
# This graph should be seen as purely relational because it doesn't take into account the difference in dining hall
# swipes for covid year and for this year. Furthermore, it doesn't discriminate between summer swipes and semester
# swipes, which are very different
weekday_means = []
for i in range(7):
	mean = NDH_data.loc[(NDH_data['Weekday'] == i) & (NDH_data['DAYPART'].isin(dayparts)), 'Swipes'].mean()
	weekday_means.append(mean)

plt.title("Averages Swipes per Day of Week")
plt.xlabel("Day of the week -- Mon = 0, Sun = 6")
plt.ylabel("Average Swipes")
plt.bar([i for i in range(7)], weekday_means)
plt.show()




# gets the mean swipes for each date with the time in daypart
dates = set()
for idx, row in NDH_data.iterrows():
	dates.add(row['BUSINESSDATE'])	
dates = list(dates)

sum_dates = []
for date in dates:
	sum_date = NDH_data.loc[(NDH_data['BUSINESSDATE'] == date) & (NDH_data['DAYPART'].isin(dayparts)), 'Swipes'].sum()
	sum_dates.append(sum_date)

plt.scatter(dates, sum_dates, s=10)
plt.show()



# Average swipes per day of week per semester
# each date is the beginning and end of classes -> this doesn't include reading days and move in days before classes
# start

for date in dates:
	print(date)

# Fall semester 2020
	# begins august 10 (2020-08-10)
	# ends november 12 (2020-11-12)
# Spring semester 2021
	# begins february 2 (2021-02-02)
	# ends may 11 (2021-05-11)
# Fall semester  2021
	# begins august 23 (2021-08-23)
	# ends december 7 (2021-12-07)
# Spring semester 2022
	# begins jauary 10 (2022-01-10)
	# ends april 26 (to end)





'''
So we have the necessary data, we need to add the weather.
We can add several things from the weather, and we have to take note of a few things
	- the weather data may not be hourly
	- wind speeds?
	- temperature?
	- condition? (fair, cloudy, light rain, ...)
'''

