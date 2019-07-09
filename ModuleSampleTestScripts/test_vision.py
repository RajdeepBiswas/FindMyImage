import sys
import os
#We need to set the sys path for the modules to be imported
parent_dir = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(parent_dir)

import Secrets.config as config
from CustomModules.Metadata.image import ImageData
from CustomModules.Vision.response import ResponseData
######################################################################################
######################################################################################
######################################################################################

#This demonstartes response.get_vision_reponse() method for local


print ("\n")
print ("-".center(100,'-')) 
print("Test CustomModules.Vision.response for local".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")

#With local image
#Can be done with remote object the same way
image_path = "C:/Users/rabiswas/Pictures/vision_test/IMG_with_location.jpg"

#Create the class object
#image_object = ImageData(is_local='Y', local_path=image_path)
#image_data  = image_object.image_data

image_data = open(image_path, "rb").read()

response = ResponseData(is_local='Y', image_data=image_data)

print (response.status)

assert(response.status is None), "reponse has failed"

print (response.get_vision_reponse())

print ("\n")
image_caption = response.get_vision_reponse()["description"]["captions"][0]["text"].capitalize()
print (image_caption)


######################################################################################
######################################################################################
######################################################################################

#This demonstartes response.get_vision_reponse() method for remote


print ("\n")
print ("-".center(100,'-')) 
print("Test CustomModules.Vision.response for remote".center(100,' '))
print ("-".center(100,'-')) 
print ("\n")


# Set image_url to the URL of an image that you want to analyze.
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \
    "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
#image_data = open(image_path, "rb").read()

response = ResponseData(image_url=image_url)

#print (response.status)

assert(response.status is None), "reponse has failed"

print (response.get_vision_reponse())

print ("\n")
image_caption = response.get_vision_reponse()["description"]["captions"][0]["text"].capitalize()
print (image_caption)
print ("\n")


######################################################################################
######################################################################################
######################################################################################

#This demonstartes response.get_vision_reponse() method for remote on blob


image_object=ImageData(blob_object='test_images/20180616_161439.jpg')

image_url = image_object.image_url

response = ResponseData(image_url=image_url)

#print (response.status)

assert(response.status is None), "reponse has failed"

print (response.get_vision_reponse())

print ("\n")
image_caption = response.get_vision_reponse()["description"]["captions"][0]["text"].capitalize()
print (image_caption)
print ("\n")
