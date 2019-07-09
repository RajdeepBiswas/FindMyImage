# -------------------------------------------------------------------------
# File: storage.py
# Name: Rajdeep Biswas
# Date: 06/06/2019
# Desc: This module will expose 'BlobOperations' class and it's methods
# Copyright (c) Rajdeep Biswas. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from PIL import Image,ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import requests
import os

import secrets_keys.config as config

# --------------------------------------------------------------------------
# Class: ImageData
# Desc: This class will expose various methods for operating on a Blob
#       object using sas token based authorization.
# Param 1: Type: String Name: account Desc: Azure Blob Storage Account Name
# Param 2: Type: String Name: key Desc: Azure Blob Storage Account Key
# --------------------------------------------------------------------------
class ImageData():
    def __init__(self, storage_account_name=None, container_name=None, blob_object=None, sas_date_expiry=None, sas_date_start=None, sas_token=None, is_local='N', local_path=None):
        if (is_local == 'N' or is_local is None):            
            self.storage_account_name = config.STORAGE_ACCOUNT_NAME if storage_account_name is None else storage_account_name
            self.container_name = config.CONTAINER_NAME if container_name is None else container_name
            self.blob_object = config.BLOB_OBJECT if blob_object is None else blob_object
            self.sas_date_expiry = config.SAS_DATE_EXPIRY if sas_date_expiry is None else sas_date_expiry
            self.sas_date_start = config.SAS_DATE_START if sas_date_start is None else sas_date_start
            self.sas_token = config.SAS_TOKEN if sas_token is None else sas_token
            self.image_url="https://{}.blob.core.windows.net/{}/{}?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se={}&st={}&spr=https,http&sig={}".format(self.storage_account_name, self.container_name, self.blob_object, self.sas_date_expiry, self.sas_date_start, self.sas_token)
            self.image = Image.open(BytesIO(requests.get(self.image_url).content))
        else:
            self.local_path = local_path
            self.image_data = open(self.local_path, "rb").read()
            self.image = Image.open(BytesIO(self.image_data))
        

    # --------------------------------------------------------------------------
    # Method: ImageData.get_image_metadata
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------
    def get_image_metadata(self, tag_name):
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

            return self.exif_data[self.tag_name]
        except Exception as e:
            return e

    #TODO: added 
    # --------------------------------------------------------------------------
    # Method: ImageData._resize_image
    # Desc: Helper function to resize the image due to cog services restriction
    # Param 1: Type: str Name: image , the image file
    # Param 2: Type: int Name: basewidth , the width of the resized image
    # --------------------------------------------------------------------------   
    def _resize_image(image,basewidth=600):

        if (round(os.stat(imge).st_size/1024) >= 5000):
            basewidth = basewidth
            img = Image.open(image)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            print("\n Image Resized!")
        else:
            img=image
        return img     

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
    # Method: ImageData.get_image_geo_data
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------
    def get_image_geo_data(self, tag_name):
        self.extracted_location_data = {}
        self.location_data = self.get_image_metadata('GPSInfo')
        #print(self.location_data)
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
