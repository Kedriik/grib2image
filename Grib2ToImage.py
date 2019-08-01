# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 20:28:33 2019

@author: Kedrowsky
"""
import numpy as np
import cv2
import json
import math
from PIL import Image
import os 
import urllib.request
from datetime import datetime
import time
Pi = 3.14159
weather_cmd = 'bin\grib2json.cmd'
weather_input_data = 'gribdata\windsigma995.anl'
weather_output_data = 'jsondata\windsigma995.json'
weather_texture = 'imagedata\windsigma995.jpg'
#date = '20190730%2F12'
now = datetime.fromtimestamp(time.time()-3600*3)
h = 0
if now.hour > 6:
    h=6
if(now.hour>12):
    h=12
if(now.hour>18):
    h=18
d = '{}{:02d}{:02d}%2F{:02d}'.format(now.year, now.month,now.day,h)
url = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t{:02d}z.pgrb2.0p25.anl&lev_0.995_sigma_level=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.{}'.format(h,d)
urllib.request.urlretrieve(url, 'gribdata\windsigma995.anl')
os.system('{} -d -o {} {}'.format(weather_cmd, weather_output_data,weather_input_data))
wind_vmax = 30.0 #   kph



def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2.0 * (value-minimum) / (maximum - minimum)
    r = (max(0.0, 255.0*(1.0 - ratio)))
    b = (max(0.0, 255.0*(ratio - 1.0)))
    g = 255 - b - r
    return r, g, b


def compute_color1(val):
    r,g,b = rgb(0.0,wind_vmax,val)
    _color = (r/255.0,g/255.0,b/255.0)
    color = ((r), (g),b)
    return color, _color

def populate_image1(data):
    image = []
    _image=[]
    nx = (data[0]['header']['nx'])
    ny = (data[0]['header']['ny'])
    numberPoints = (data[0]['header']['numberPoints']);
    for i  in range(numberPoints):
        val, _val = compute_color1(math.sqrt(math.pow(data[0]['data'][i],2)+math.pow(data[1]['data'][i],2)))
        for c in range(len(val)):
            image.append(val[c]);
            _image.append(_val[c]);
    
    image = np.array(image);
    image = image.reshape(ny,nx,3);
    _image = np.array(_image);
    _image = _image.reshape(ny,nx,3);
    image1 = image[0:ny, 0:int(nx/2)]
    _image1 = _image[0:ny, 0:int(nx/2)]        
    image2 = image[0:ny, int(nx/2):nx]
    _image2 = _image[0:ny, int(nx/2):nx]        
    image=np.concatenate((image2, image1), axis=1)
    _image=np.concatenate((_image2, _image1), axis=1)
    return image, _image
  
with open(weather_output_data) as json_file:
    data = json.load(json_file)                
    image, _image = populate_image1(data)
    while True:
        cv2.imshow('',_image)
        if cv2.waitKey(25) & 0xFF==ord('q'):
            cv2.destroyAllWindows()
            break
    cv2.imwrite(weather_texture, image)       