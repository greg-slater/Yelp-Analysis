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
   
 
def table_creator(data, categories, days, time_range, csv):


    output = []
    
    # loop through days in range
    for day in days:
        # loop through hours in defined range
        for time in time_range:
        
            out = dict()
            
            # loop through business categories in file
            for category in categories:
                count = 0
                # loop through business dictionaries  for current category
                for key in data[category]:
                    
                    # try to return hours for current day - not every business will have this data
                    try:
                        hs = key['hours'][str(day)]
    
                        s = pd.to_datetime(hs['start']).time()
                        e = pd.to_datetime(hs['end']).time()
                        
                        # check if  business times cross midnight, if so time needs only be either less than close or more than open, not both
                        if e < s and (time < e or time > s):
                                count += 1
                        
                        # else time must be between open and close for count to go up
                        elif time > s and time < e:
                            count += 1
                        
                    # skip if no data for current day
                    except Exception:
                        pass
                    
                # add the count for category to the dictionary           
                out[category] = count
               
            # add current time and day to the dictionary    
            out['time'] = time.isoformat()
            out['day'] = day
            # append dictionary to output before loop starts again
            output.append(out)
    
    table = pd.DataFrame(output)

    if csv == True:
        table.to_csv('venue_hours_table_output.csv')
        
    return table


#%%

# EXAMPLE
    
# load in test dataset
with open('business_hours_formatted.json') as f:
    data = json.load(f)

# set time range
time_range = pd.date_range('00:00', '23:00',  freq='60 min').time
print(time_range)

# define categories
categories = ['musicvenues', 'pubs']

# define day range
days = list(range(0,7))

# run function
table_creator(data, categories, days, time_range, csv=True)





#%% WORKINGS

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
                try:
                    hs = key['hours'][str(day)]

                    s = pd.to_datetime(hs['start']).time()
                    e = pd.to_datetime(hs['end']).time()
                    
                    # check if  business times cross midnight, if so time needs only be either less than close or more than open, not both
                    if e < s and (time < e or time > s):
                            count += 1
                    
                    # else time must be between open and close for count to go up
                    elif time > s and time < e:

                        count += 1
                        
                except Exception:
                    pass
                
            # add the count for category to the dictionary           
            out[category] = count
           
        # add current time and day to the dictionary    
        out['time'] = time.isoformat()
        out['day'] = day
        # append dictionary to output before loop starts again
        output.append(out)

output

table = pd.DataFrame(output)

table

data['musicvenues'][0]
len(data['musicvenues'])

t2 = t + pd.DateOffset(1)
time_range
t2

#%%



