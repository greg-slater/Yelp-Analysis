# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 08:41:12 2018

@author: Greg
"""

import datetime as dt
import pandas as pd
import json

def convert_time(time_in):
    
    h = int(time_in[0:2])
    m = int(time_in[2:4])
    time_out = dt.time(h,m)
    
    return time_out

s_time = convert_time('1100')
e_time = convert_time('2045')

interval = convert_time('0030')

print(s_time)
print(e_time)

r = pd.date_range('01/01/2018 00:00', '01/02/2018 00:00',  freq='45 min').time
print(r)

s_time >= r[0] and s_time <= r[-1]

#%%

with open('test_all_businesses.json') as f:
    data = json.load(f)
    
for key in data['music_venues']:
    
    for key2 in key['hours']:
        
        o = convert_time(key2['start']).isoformat()
        c = convert_time(key2['end']).isoformat()
        
        key2['open'] = o
        key2['close'] = c
        
        del key2['start']
        del key2['end']
        
print(data)
        
for key in data['pubs']:
    
    for key2 in key['hours']:
        
        o = convert_time(key2['start']).isoformat()
        c = convert_time(key2['end']).isoformat()
        
        key2['open'] = o
        key2['close'] = c
        
        del key2['start']
        del key2['end']

with open('test_all_businesses_2.json', 'w') as f:
    json.dump(data, f, indent=2)
print(data)
        

t = dt.time(22)


for key in data['music_venues']:
    
    for key2 in key['hours']:
        
#        t = pd.to_datetime(key2['close']).time()
#        print(t)
        
        if t >= pd.to_datetime(key2['open']).time() and t <= pd.to_datetime(key2['close']).time():
            
            print('true')
        
        
        
        