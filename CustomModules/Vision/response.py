# -------------------------------------------------------------------------
# File: response.py
# Name: Rajdeep Biswas
# Date: 07/09/2019
# Desc: This module will computer vision and expose the response
# Copyright (c) Rajdeep Biswas. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import sys
import os
import requests
import json

#We need to set the sys path for the modules to be imported
parent_dir = os.path.abspath(os.path.join(os.getcwd(),"../.."))
sys.path.append(parent_dir)

import Secrets.config as config

# --------------------------------------------------------------------------
# Class: ResponseData
# Desc: This class will expose various methods for operating on a Blob
#       object using sas token based authorization.
# Params: Remote image params are by default taken from config
# Param 1: Type: String Name: analyze_url Desc: Azure Blob Storage Account Name
# Param 2: Type: String Name: headers Desc: Blob Storage Conatiner name
# Param 3: Type: String Name: params Desc: Blob Storage File name
# Param 4: Type: String Name: image_url Desc: Blob Storage SAS expiry date
# Param 5: Type: String Name: image_data Desc: Blob Storage SAS start date
# --------------------------------------------------------------------------
class ResponseData():
    def __init__(self, analyze_url=None, headers=None, params=None, \
        image_url=None, image_data=None, \
        is_local='N', local_path=None):
        self.analyze_url = config.ANALYZE_URL \
            if analyze_url is None else analyze_url
        self.params = config.PARAMS \
            if params is None else params        
        if (is_local == 'N' or is_local is None):   
            self.headers = config.HEADERS_REMOTE \
                 if headers is None else headers            
            self.image_url = image_url              
            self.data = {'url': image_url}         
            self.response = requests.post(self.analyze_url, headers=self.headers, params=self.params, json=self.data)
            self.status = self.response.raise_for_status()
            #return self
        else:
            self.headers = config.HEADERS_LOCAL \
                 if headers is None else headers                
            self.image_data = image_data
            self.response = requests.post(self.analyze_url, headers=self.headers, params=self.params, data=self.image_data)
            self.status = self.response.raise_for_status()
            #return self

    # --------------------------------------------------------------------------
    # Method: Response.get_vision_reponse
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    #                          default value is 'All'
    # Returns: The value of the metadata or a hash containing all metadata
    #            in key and values
    # --------------------------------------------------------------------------
    def get_vision_reponse(self, tag_name='All'):
        self.response_json = self.response.json()
        self.tag_name = tag_name
        try:
            if tag_name == 'All':
                return self.response_json
            else:
                return self.response_json[self.tag_name]
        except Exception as e:
            return e            
        