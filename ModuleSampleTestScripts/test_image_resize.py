import sys
import os
#We need to set the sys path for the modules to be imported
parent_dir = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(parent_dir)

import Secrets.config as config

from CustomModules.Metadata.image import ImageData

######################################################################################
######################################################################################
######################################################################################


#Test4: Image resize
#This demonstartes ImageData.resize_image() method


#With local image
#Can be done with remote object the same way
image_path = "C:/Users/rabiswas/Pictures/vision_test/20180114_153550_HDR.jpg"

#Create the class object
image_object = ImageData(is_local='Y', local_path=image_path)

print ("\n")
print ("-".center(100,'-'))    
print("Get resized image".center(100,' '))
print ("-".center(100,'-'))  
print ("\n")

###
print (image_object.image.size)
resized_image=image_object.resize_image()
resized_image.save('C:/Users/rabiswas/Pictures/vision_test/resized_image_prop.jpg')
print (resized_image.size)


print ("size double test!!")
#In this test we will try to make the image double its original size

print (image_object.image.size)
resized_image=image_object.resize_image(2)
resized_image.save('C:/Users/rabiswas/Pictures/vision_test/resized_image_2x.jpg')
print (resized_image.size)