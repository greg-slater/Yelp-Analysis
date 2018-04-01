# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:33:40 2018

@author: Greg
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:57:13 2018

@author: Greg
"""

import json
import pandas as pd

#%%
# this function allows you to query the Yelp dataset
# define the dataset, the categories to output, and a time range (between 0 - 2400)
# it will output a table with the number of businesses in each category open at each
# time in the range, and optionally create a csv as well
# (note - just built for one day of the week at the moment, but can extend to do all at once)
    
def table_creator(data, categories, start_hour, end_hour, step, csv):

    day = 0
    output = []
    
    # loop through hours in defined range
    for mins in range(start_hour, end_hour, step):
    
        d = dict()
        
        # loop through business categories in file
        for category in categories:
            count = 0
            # loop through business dictionaries  for current category
            for key in data[category]:
                # loop through days 0-6 in the 'hours' dictionary for each business
                for key2 in key['hours']:
                    
                  # if the day matches and the time is between start and end add to count
                   if key2['day'] == day and int(key2['start']) <= mins and int(key2['end']) >= mins:
                       
                       count += 1
            
            # add the count for category to the dictionary           
            d[category] = count
            
        # add current time to the dictionary    
        d['time'] = str(mins)
        # append dictionary to output before loop starts again
        output.append(d)
    
    # create table from dictionary and set time as index
    table = pd.DataFrame(output).set_index('time')
    
    if csv == True:
        table.to_csv('venue_hours_table_output.csv')
        
    return table

#%%

# EXAMPLE
    
# load in test dataset
with open('business_hours_formatted.json') as f:
    data = json.load(f)
    
time_range = pd.date_range('00:00', '23:00',  freq='60 min').time
print(time_range)

    
# set categories (currently only ones in test file)
categories = ['musicvenues', 'pubs']

# run for each hour of the day and output csv
table_creator(data, cats, 0, 2460, 60, csv=True)



day = 0


output = []

for day in range(0, 7):
    # loop through hours in defined range
    for time in time_range:
    
        out = dict()
        
        # loop through business categories in file
        for category in categories:
            count = 0
            # loop through business dictionaries  for current category
            for key in data[category]:
                # loop through days 0-6 in the 'hours' dictionary for each business
                for key2 in key['hours']:
                    
                    d = key2['day']
                    start = pd.to_datetime(key2['start']).time()
                    end = o = pd.to_datetime(key2['end']).time()
                    
                    if day == d and time >= start and time <= end:
                        
                        count += 1
                    
    #              # if the day matches and the time is between start and end add to count
    #               if key2['day'] == day and int(key2['start']) <= mins and int(key2['end']) >= mins:
    #                   
    #                   count += 1
    #        
            # add the count for category to the dictionary           
            out[category] = count
           
        # add current time and day to the dictionary    
        out['time'] = time.isoformat()
        out['day'] = day
        # append dictionary to output before loop starts again
        output.append(out)

output

