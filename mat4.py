# -*- coding: utf-8 -*-
"""
Created on Fri May  7 18:00:01 2021

@author: Noamc
"""

api_key = "Please enter the api key"

import json, requests, urllib
from urllib.parse import urlparse
import pandas as pd



def open_file(path):
    return open(path ,'r', encoding="utf-8") 

file = open_file("C:/Users/Noamc/Downloads/dests.txt")

destinations_distances_dict = dict()
tup = tuple
results = dict() 
destination_counter = 0

for line in file:
    if destination_counter > 5:
        break
    else:
        dictionary = dict()
        destination = line
        serviceurl_distancematrix = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        serviceurl_geocode ="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (destination,api_key)
        dictionary = {'origins' : 'תל אביב' ,
                      'destinations' : destination ,
                      'key' : api_key }
        url_distancematrix = serviceurl_distancematrix + urllib.parse.urlencode(dictionary)
        response_geocode_json = requests.get(serviceurl_geocode).json()
        response_goecode_dump = json.dumps(response_geocode_json)
        response_geocode = json.loads(response_goecode_dump)
        
        try:
            if not response_geocode["status"] == "OK":
                print("HTTP error")
            else:
                try:
                    response_geocode = json.loads(response_goecode_dump)
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")
            
        try:
            response_dist = requests.get(serviceurl_geocode)
            if not response_dist.status_code == 200:
                print("HTTP error",response_dist.status_code)
            else:
                try:
                    response_data = response_dist.json()
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")  
            
        response_data = requests.get(url_distancematrix).json()
        response_data_new = json.dumps(response_data)
        response_data_new = json.loads(response_data_new)
        
        longitude = response_geocode['results'][0]['geometry']['location']['lng'] ##longitude
        
        latitude = response_geocode['results'][0]['geometry']['location']['lat'] ##latitude
        
        distance = response_data_new["rows"][0]["elements"][0]["distance"]["text"] ##distance
        distance_str = distance.split()[0]
        distance_int = distance_str.replace(',', '')
        
        duration = response_data_new["rows"][0]["elements"][0]["duration"]["value"] ##duration
        durationNew=(duration / 3600)   ##hour VS. min
        duration_hours = int(durationNew)
        calc_minutes = durationNew - duration_hours
        duration_minutes = int(float('%.2f' % (calc_minutes))*60 )
        total_duration = str(duration_hours)+" hours and " +str(duration_minutes)+" minutes"
        
        tup = (distance_str+" km", total_duration , longitude, latitude)
        destinations_distances_dict[destination.rstrip()] = distance_int
        results[destination.rstrip()] = (tup)
        
        destination_counter += 1
        
if destination_counter==5:
    list_destinations_distances = [] 
    for distance,destination in sorted(destinations_distances_dict.items()):
        swaped_tuple = (destination, distance)
        list_destinations_distances.append(swaped_tuple)  
    list_destinations_distances = sorted(list_destinations_distances, reverse=True)
    dataframe = pd.DataFrame.from_dict(results, orient='index',columns=['Distance', 'Duration', 'Longtitude', 'Latitude'])
    display(dataframe)
    sorted_list = pd.DataFrame(list_destinations_distances, columns=['Distance','Destination'])
    print("שלושת הערים הכי רחוקות מתל אביב :")
    display(sorted_list[0:3])
else:
    print("must have 5 destinations")


    
     