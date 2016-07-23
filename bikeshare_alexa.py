# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 14:01:21 2016

@author: dokbr

An alexa app to check on the status of nearby capital bikeshare stations
"""

import xml.etree.ElementTree as ET
import httplib, urllib, urllib2, base64


def Get_station_data():
    # get the xml as a string
    try:
        conn = httplib.HTTPSConnection('www.capitalbikeshare.com')
        conn.request("GET", "/data/stations/bikeStations.xml")
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    # put it into an ET object
    root = ET.fromstring(data)
    return root


# some user parameters
Read_empty_stations = True
Read_number_of_docks = False

# define a dictionary of stops and plain language names in the order
# that you want Alexa to read them.

station_dict = {31115: "Columbia", 31102: "Kenyon", 31105: "Harvard", 31207: "Fairmont"}