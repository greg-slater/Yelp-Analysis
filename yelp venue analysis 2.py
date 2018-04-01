# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 11:42:35 2018

@author: Greg
"""

import numpy as np
import json
import yelp_api 
yp = yelp_api

#%%
# test response
result = yp.search('london', 'hotelstravel', 0, 50)
result


#%% 
def get_businesses_multi(city, categories):

    dict_out = {}
    
    for cat in categories:
        
        dict_out[cat] = []
        
        # make initial request to get the total number of business results
        check = yp.search(city, cat, 1, 0)
        
        total = check['total']
        
        if total > 1000:
            print('total businesses greater than 1,000, only first 1,000 results will be returned')
            total = 999
            
        else:
            print('total businesses = ', total)
        
        # set max number of  results that can be returned at one time
        results = 50
        # offset will be incremented to run through results up to total
        offset = 0
        
        full_requests = int(np.floor(total/results))
        remaining_requests = total%results
            
            # run through full requests + 1 extra for the remainder
        for i in range(1, full_requests + 2):
            
            # request 50 results while still in full range
            if i <= full_requests:
                print('Category:           ', cat)
                print('Type:                  full')
                print('Request number: ', i, ' out of ', full_requests+1)
                print('Offset:                ', offset)
                request = yp.search(city, cat, results, offset)
                print()
                
            # else just grab the remainder 
            if i > full_requests:
                print('Category:           ', cat)
                print('Type:                  partial')
                print('Request number: ', i, ' out of ', full_requests+1)
                print('Offset:                ', offset)
                request = yp.search(city, cat, remaining_requests, offset)
                print()
                
            # increment the offset each loop
            offset += results
            
            # extend category array of dictionary with businesses from each request
            dict_out[cat].extend(request['businesses'])
            
    return dict_out
#%%

cats = ['musicvenues', 'pubs', 'restaurants']
city = 'london'

full_results = get_businesses_multi(city, cats)

with open('full_results.json', 'w') as f:
    json.dump(full_results, f, indent=2)

#%%
# format and save full results

full_results_formatted = dict()

for cat in cats:
    full_results_formatted[cat] = []

    # run through businesses within category
    for key in full_results[cat]:
        # create a dictionary with the keys we need
        d = dict()
        d['name'] = key['name']
        d['id'] = key['id']
        d['coordinates'] = key['coordinates']
#        print(cat)
#        print(key['name'])
#        print()
    
        # append the new dictionary into the list in main one
        full_results_formatted[cat].append(d)
    

with open('full_results_formatted.json', 'w') as f:
    json.dump(full_results_formatted, f, indent=2)
    

#%%
# FIND OPENING HOURS FOR VENUES
# warning this will query the Yelp API once for each business in your output from above

# test output
#out = yp.business(full_results_formatted['pubs'][183]['id'])

yp.business('the-amersham-arms-london')

business_hours = dict()

for cat in cats:
    
    print(cat)
    print('...')
    business_hours[cat] = []
    
    for i, key  in enumerate(full_results_formatted[cat]):
        
        try:
            name = key['id']
            d = yp.business(name)
            business_hours[cat].append(d)
#            print(i)
#            print(name)
            
        except Exception:
            print('error at ', cat, ' - ', name, ' index no. ', i)
            pass
        
d
    
with open('business_hours.json', 'w') as f:
    json.dump(business_hours, f, indent=2)

#%%
    
def convert_time(time_in):

    h = int(time_in[0:2])
    m = int(time_in[2:4])
    time_out = dt.time(h,m)

    return time_out


#%%
# CREATE NEW FILE WITH VENUE DETAILS AND OPENING HOURS
    
# test format
#business_hours['pubs'][0]['hours'][0]['open']

business_hours_formatted = dict()

for cat in cats:
    
    business_hours_formatted[cat] = []

    for key in business_hours[cat]:
        
        d = dict()  # blank dictionary to populate
        hours = []
        
        # try and find hours or skip
        try:
            h = key['hours'][0]['open']  # identify opening hours array
            
            # cycle through days and append hours to lists
            for days in h:
                
                hs = dict()
                hs['day'] = days['day']
                hs['start'] = convert_time(days['start']).isoformat()
                hs['end'] = convert_time(days['end']).isoformat()
                
                hours.append(hs)
    
            # build dictionary and append to list
            d['name'] = key['name']
            d['coordinates'] = key['coordinates']
            d['id'] = key['id']
            d['hours'] = hours
            
            business_hours_formatted[cat].append(d)
        
        except KeyError:
            print()
        
#test retrieve
#business_hours_formatted['restaurants'][960]

with open('business_hours_formatted.json', 'w') as f:
    json.dump(business_hours_formatted, f, indent=2)
    