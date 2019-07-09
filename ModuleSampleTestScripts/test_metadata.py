import sys
import os
#We need to set the sys path for the modules to be imported
parent_dir = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(parent_dir)

import Secrets.config as config

from Module.Metadata.image import ImageData

#Test1: With local image
#This demonstartes ImageData.get_image_geo_data() method

image_path = "C:/Users/rabiswas/Pictures/vision_test/IMG_with_location.jpg"

#Create the class object
image_object = ImageData(is_local='Y', local_path=image_path)

#Get the polished GPS information 
#We still need to decode the point in GPS to more precise location using Maps API
#Note: For this to work the GPS must be on while taking the pictures which embeds 
###### the information in Exif format.
print ("\n")
print ("-".center(100,'-'))    
print("Local test started".center(100,' '))
print ("-".center(100,'-'))  
print ("\n")

#Latitude: 28.96817172222222
#Longitude: -95.26418063888889
#Coordinates: 28.96817172222222,-95.26418063888889
latitude=image_object.get_image_geo_data('Latitude')
print ("Latitude: {}".format(latitude))
longitude=image_object.get_image_geo_data('Longitude')
print ("Longitude: {}".format(longitude))
coordinates=image_object.get_image_geo_data('Coordinates')
print ("Coordinates: {}".format(coordinates))

print ("\n")
print ("-".center(100,'-'))     
print("Local test finished".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")


######################################################################################
######################################################################################
######################################################################################


#Test2: With image stored in Blob accessed using SAS
#This demonstartes ImageData.get_image_geo_data() method

print ("\n")
print ("-".center(100,'-'))     
print("Remote test started".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")

#Create the class object
#Option 1: Pass all parameters
#image_object=ImageData(config.STORAGE_ACCOUNT_NAME, config.CONTAINER_NAME, config.BLOB_OBJECT, config.SAS_DATE_EXPIRY, config.SAS_DATE_START, config.SAS_TOKEN)

#Option 2: Pass no parameters when it will read from config
#image_object=ImageData()

#Option 3: Pass what you prefer
#For example we will pass a blob file name which is going to be the most common scenario
image_object=ImageData(blob_object='test_images/20180616_161439.jpg')

#Get the polished GPS information 
#We still need to decode the point in GPS to more precise location using Maps API
#Note: For this to work the GPS must be on while taking the pictures which embeds 
###### the information in Exif format.

#Latitude: 29.539763
#Longitude: -95.60122127777777
#Coordinates: 29.539763,-95.60122127777777
latitude=image_object.get_image_geo_data('Latitude')
print ("Latitude: {}".format(latitude))
longitude=image_object.get_image_geo_data('Longitude')
print ("Longitude: {}".format(longitude))
coordinates=image_object.get_image_geo_data('Coordinates')
print ("Coordinates: {}".format(coordinates))

print ("\n")
print ("-".center(100,'-')) 
print("Remote test finished".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")


######################################################################################
######################################################################################
######################################################################################


#Test3: Get All metadata from the exif associated with the image
#This demonstartes ImageData.get_image_metadata() method


#With local image
#Can be done with remote object the same way
image_path = "C:/Users/rabiswas/Pictures/vision_test/IMG_with_location.jpg"

#Create the class object
image_object = ImageData(is_local='Y', local_path=image_path)

print ("\n")
print ("-".center(100,'-'))    
print("Get all metdata".center(100,' '))
print ("-".center(100,'-'))  
print ("\n")

metadata_hash=image_object.get_image_metadata()

print (metadata_hash)

#The metadata_hash, has keys like
""" 
ExifImageWidth
ExifImageHeight
DateTimeOriginal
DateTimeDigitized
Make
Model
ExifVersion
ShutterSpeedValue
ApertureValue
BrightnessValue
ExposureBiasValue
MaxApertureValue
FocalLength
Saturation
ISOSpeedRatings
DigitalZoomRatio
Contrast
Sharpness
WhiteBalance 
 """

#So you can either print it from the hash or call it individually

#Image width: 2340 Image Height: 4160
print ("Image width: {} Image Height: {}".\
    format(metadata_hash['ExifImageWidth'],metadata_hash['ExifImageHeight']))
#Image is taken from: Motorola Moto G (4) on date: 2017:03:18 16:33:54
print ("Image is taken from: {} {} on date: {}".\
    format(metadata_hash['Make'],metadata_hash['Model'],metadata_hash['DateTimeOriginal']))


#Calling it individually (Might want to avoid multiple calls)    
#Image width: 2340 Image Height: 4160
print ("Image width: {} Image Height: {}".\
    format(image_object.get_image_metadata('ExifImageWidth'), \
        image_object.get_image_metadata('ExifImageHeight')))

print ("\n")
print ("-".center(100,'-')) 
print("Get all metdata test finished".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")
