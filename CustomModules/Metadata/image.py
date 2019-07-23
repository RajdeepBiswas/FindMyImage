# -------------------------------------------------------------------------
# File: image.py
# Name: Rajdeep Biswas
# Date: 07/08/2019
# Desc: This module will read image files and expose it's metadata
# Copyright (c) Rajdeep Biswas. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from PIL import Image,ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import requests
import sys
import os

#We need to set the sys path for the modules to be imported
parent_dir = os.path.abspath(os.path.join(os.getcwd(),"../.."))
sys.path.append(parent_dir)

import Secrets.config as config

# --------------------------------------------------------------------------
# Class: ImageData
# Desc: This class will expose various methods for operating on a Blob
#       object using sas token based authorization.
# Params: Remote image params are by default taken from config
# Param 1: Type: String Name: storage_account_name Desc: Azure Blob Storage Account Name
# Param 2: Type: String Name: container_name Desc: Blob Storage Conatiner name
# Param 3: Type: String Name: blob_object Desc: Blob Storage File name
# Param 4: Type: String Name: sas_date_expiry Desc: Blob Storage SAS expiry date
# Param 5: Type: String Name: sas_date_start Desc: Blob Storage SAS start date
# Param 6: Type: String Name: sas_token: Blob Storage SAS token
# Param 7: Type: String Name: is_local Desc: Local file flag. Default = 'N'
# Param 8: Type: String Name: local_path Desc: Local file path
# --------------------------------------------------------------------------
class ImageData():
    def __init__(self, storage_account_name=None, container_name=None, \
                    blob_object=None, sas_date_expiry=None, sas_date_start=None, \
                        sas_token=None, is_local='N', local_path=None):
        if (is_local == 'N' or is_local is None):            
            self.storage_account_name = config.STORAGE_ACCOUNT_NAME \
                if storage_account_name is None else storage_account_name
            self.container_name = config.CONTAINER_NAME \
                if container_name is None else container_name
            self.blob_object = config.BLOB_OBJECT \
                if blob_object is None else blob_object
            self.sas_date_expiry = config.SAS_DATE_EXPIRY \
                if sas_date_expiry is None else sas_date_expiry
            self.sas_date_start = config.SAS_DATE_START \
                if sas_date_start is None else sas_date_start
            self.sas_token = config.SAS_TOKEN \
                if sas_token is None else sas_token
            self.image_url="https://{}.blob.core.windows.net/{}/{}?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se={}&st={}&spr=https,http&sig={}"\
                .format(self.storage_account_name, self.container_name, self.blob_object, \
                         self.sas_date_expiry, self.sas_date_start, self.sas_token)
            self.image = Image.open(BytesIO(requests.get(self.image_url).content))
        else:
            self.local_path = local_path
            self.image_data = open(self.local_path, "rb").read()
            self.image = Image.open(BytesIO(self.image_data))
        

    # --------------------------------------------------------------------------
    # Method: ImageData.get_image_metadata
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    #                          default value is 'All'
    # Returns: The value of the metadata or a hash containing all metadata
    #            in key and values
    # --------------------------------------------------------------------------
    def get_image_metadata(self, tag_name='All'):
        self.exif_data = {}
        self.tag_name = tag_name
        try:
            info = self.image._getexif()
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for gps_tag in value:
                            sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[sub_decoded] = value[gps_tag]

                        self.exif_data[decoded] = gps_data
                    else:
                        self.exif_data[decoded] = value
            if tag_name == 'All':
                return self.exif_data
            else:
                return self.exif_data[self.tag_name]
        except Exception as e:
            return e
            
    # --------------------------------------------------------------------------
    # Method: ImageData._decimal_conversion
    # Desc: Helper function to convert the GPS coordinates to decimal
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------           
    def _decimal_conversion(self, value):
        deg_num, deg_denom = value[0]
        v_degrees = float(deg_num) / float(deg_denom)

        min_num, min_denom = value[1]
        v_minutes = float(min_num) / float(min_denom)

        sec_num, sec_denom = value[2]
        v_seconds = float(sec_num) / float(sec_denom)
        
        return v_degrees + (v_minutes / 60.0) + (v_seconds / 3600.0)

    # --------------------------------------------------------------------------
    # Method: ImageData.resize_image
    # Desc: Helper function to resize the image due to cog services restriction
    # Param 1: Type: float Name: resize_percentage 
    # --------------------------------------------------------------------------   
    def resize_image(self,resize_percentage=None,):

        #Because JpegImageFile' object has no attribute 'st_size'
        if (self.is_local == 'N' or self.is_local is None):
            site = urllib.request.urlopen(self.image_url)
            meta = site.info()
            self.size_kb = float(meta.get("Content-Length"))/1024            
        else:
            self.size_kb = round(os.stat(self.local_path).st_size/1024)
        if (self.size_kb >= 5000 or resize_percentage is not None):
            #its 5 MB but for safety we took 4.9 MB
            self.resize_percentage = 4900 / self.size_kb \
                if resize_percentage is None else \
                    resize_percentage
            self.width = self.image.size[0]
            self.height = self.image.size[1]
            self.resized_width = int(self.width * self.resize_percentage)
            self.resized_height = int(self.height * self.resize_percentage)
            self.resized_image = self.image.resize((self.resized_width,self.resized_height), Image.ANTIALIAS)
            self.orientation =  self.get_image_metadata('Orientation')
            if self.orientation == 3:
                self.touched_image = self.resized_image.rotate(180,expand=True)
            elif self.orientation == 6:
                self.touched_image = self.resized_image.rotate(270,expand=True)
            elif self.orientation == 8:
                self.touched_image = self.resized_image.rotate(90,expand=True)
            else:
                self.touched_image = self.resized_image
        else:
            self.touched_image=self.image
        return self.touched_image    

    
    # --------------------------------------------------------------------------
    # Method: ImageData.get_image_geo_data
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: Extracts Latitude,Longitude and
    #                                                Coordinates
    # --------------------------------------------------------------------------
    def get_image_geo_data(self, tag_name):
        self.extracted_location_data = {}
        self.location_data = self.get_image_metadata('GPSInfo')
        self.latitude = None
        self.longitude = None
        self.tag_name = tag_name        
        self.gps_latitude = self.location_data.get("GPSLatitude")
        self.gps_latitude_ref = self.location_data.get('GPSLatitudeRef')
        self.gps_longitude = self.location_data.get('GPSLongitude')
        self.gps_longitude_ref = self.location_data.get('GPSLongitudeRef')

        if self.gps_latitude and self.gps_latitude_ref and self.gps_longitude and self.gps_longitude_ref:
            self.latitude = self._decimal_conversion(self.gps_latitude)
            if self.gps_latitude_ref != "N":                     
                self.latitude *= -1

            self.longitude = self._decimal_conversion(self.gps_longitude)
            if self.gps_longitude_ref != "E":
                self.longitude *= -1
        self.extracted_location_data['Latitude'] = self.latitude
        self.extracted_location_data['Longitude'] = self.longitude
        self.extracted_location_data['Coordinates'] = "{},{}".format(self.latitude,self.longitude)
        try:  
            return self.extracted_location_data[self.tag_name]
        except Exception as e:
            return e            

    def __del__(self):
        pass
