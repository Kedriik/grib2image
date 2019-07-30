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

Pi = 3.14159
weather_cmd = 'bin\grib2json.cmd'
weather_input_data = 'gribdata\windsigma995.anl'
weather_output_data = 'jsondata\windsigma995.json'
weather_texture = 'imagedata\windsigma995.jpg'

os.system('{} -d -o {} {}'.format(weather_cmd, weather_output_data,weather_input_data))

def compute_color1(val):
    red_offset = 0.0#35.0;
    green_offset = 0.0#25.0;
    blue_offset = 0.0#7.5;
    val = math.log(val+1)/4.0
    r = math.cos(val);
    g = math.sin(val);
    b = val;
    color = (255.0*(r), 255.0*(g),255.0*b)
    _color = ((r), (g),b)
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

def populate_image2(data):
    image = []
    _image=[]
    x = 0;
    for i in range((data[0]['header']['numberPoints'])):
        val = (math.sqrt(math.pow(data[x]['data'][i],2)+math.pow(data[x+1]['data'][i],2)))
        val = val/10.0
        image.append(val)
        _image.append(val);
    image = np.array(image);
    image = image.reshape(181,360,1);
    _image = np.array(_image);
    _image = _image.reshape(181,360,1);
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