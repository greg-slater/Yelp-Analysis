import numpy as np
import json
import yelp_api 
yp = yelp_api

#%%
result = yp.search('london', 'musicvenues', 1, 0)
result['total']
#print(yp.business('royal-albert-hall-kensington'))
#%%

# Request API in offset increments of 50 and load results into list
music_venues = []

results = 50
offset = 0
total = 283

full_requests = np.floor(total/results)
remaining_requests = total%results

for i in range(1,7):
    
    if i <= full_requests:
        
        d = yp.search('london', results, offset)
        
    else:
        
        d = yp.search('london', remaining_requests, offset)
        
    offset = offset + results
    
    music_venues.extend(d['businesses'])


#%%
# create a new dictionary and an empty list within

new_file = dict()
new_file['businesses'] = []

# the enumerate here just means an index key can be used as well
for index, keys in enumerate(music_venues):
    # create a dictionary with the keys we need
    d = dict()
    d['name'] = keys['name']
    d['id'] = keys['id']
    d['coordinates'] = keys['coordinates']
    #d['open'] = c[index]
    
    # append the new dictionary into the list in main one
    new_file['businesses'].append(d)
    

#new_json = json.dump(new_file)

with open('music_venues.json', 'w') as f:
    json.dump(new_file, f, indent=2)
    
new_file[0]
#%%
# FIND OPENING HOURS FOR VENUES
# warning this will query the Yelp API once for each business in your output from above

hours_file = []

for key in new_file['businesses']:
    name = key['id']
    d = yp.business(name)
    hours_file.append(d)

#%%
# CREATE NEW FILE WITH VENUE DETAILS AND OPENING HOURS

venue_hours = dict()
venue_hours['venues'] = []

for key in hours_file:
    
    d = dict()  # blank dictionary to populate
    s = []
    e = []
    hours = []
    
    # try and find hours or skip
    try:
        h = key['hours'][0]['open']  # identify opening hours array
        
        # cycle through days and append hours to lists
        for days in h:
            
            hs = dict()
            hs['day'] = days['day']
            hs['start'] = days['start']
            hs['end'] = days['end']
            
            hours.append(hs)
        
        # build dictionary and append to list
        d['name'] = key['name']
        d['coordinates'] = key['coordinates']
        d['id'] = key['id']
        d['hours'] = hours
        
        venue_hours['venues'].append(d)
    
    except KeyError:
        print()


with open('venues_hours.json', 'w') as f:
    json.dump(venue_hours, f, indent=2)
