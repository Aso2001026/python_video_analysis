import glob
import os

# Get all image files in images path
# I puted not moving shuttle images in shuttle-not-moving folder
# If you want to rename other images, change path
path = '../image/shuttle-not-moving'

file_count = 1

filelist = glob.glob(path+'/*.png')
print(filelist)

for file in filelist:
    os.rename(file, path + '/' + str(file_count) + '.png')
    file_count += 1

filelist = glob.glob(path+'/*.png')
print("after rename")
print(filelist)

