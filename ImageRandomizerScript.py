from PIL import Image
import os, re
import random 
import numpy as np
from pathlib import Path

def GetShuffleImagesBool():
    # Get whether to shuffle images or not
    shuffleItems = input("Shuffle images? Yes or No: ")
    if shuffleItems == "Yes":
        return True
    if shuffleItems == "No":
        return False
    
def get_file_key(filename):
    key = re.sub("[^0-9]", "", filename)
    if bool(re.search(r'\d', filename)):
        return int(key)

def sort_filenames(all_files):
    filenames_sorted = []
    original_filenames = {}
    for full_filename in all_files:
        filename, file_extension = os.path.splitext(full_filename)

        # Save all the files names to be sorted
        filenames_sorted.append(filename)
        # Save original full filename in a dictionary for later retrieval
        original_filenames[filename] = full_filename

    # Sort the list using key
    filenames_sorted.sort(key=get_file_key)
    filenames = []
    for key in filenames_sorted:
        filenames.append(original_filenames[key])

    return filenames

def ReoutputImages(outputFolder: str, folder: str, folderCount: int,  my_list: int, imageName: str):
    number = 0
    # Create an ordered list for all items in the folder
    index = 0
    fileList = [None] * (folderCount)
    for filename in os.listdir(folder):
        if not filename == 'output':
            fileList[index] = filename
            index += 1
    sortedFiles = sort_filenames(fileList)

    # Rename the items
    for filename in sortedFiles:
        if not filename == 'output':
            imgbg = Image.open(folder + filename)
            newimg = imgbg

        # Recreate if it is a Gif
        if imgbg.is_animated:
            frames = []
            for num in range(imgbg.n_frames):
                imgbg.seek(num)
                text_img = Image.new('RGBA', (1200,1200), (0, 0, 0, 0))
                text_img.paste(imgbg, (0,0))
                frames.append(text_img)
                temp_num = my_list[number]
            frames[0].save(outputFolder + imageName + str(temp_num) + '.gif',
                    save_all=True,
                    append_images=frames[1:],
                    duration=100,
                    loop=0)  
        else:
            temp_num = my_list[number]
            newimg.save(outputFolder + imageName + str(temp_num) + '.png', 'PNG')
        number += 1

# Get directory
home = str(Path.home()) + '\\'

# Get folder location and image name input from user
folderLocation = str(input("Enter images file location: "))
imageName = str(input("Enter a name to give all Images, if none then just press enter: "))
folder = home + folderLocation + '\\'

# Checking if the directory demo_folder 
# Exist or not.
if not os.path.exists(folder+"output\\"):
    # If the folder directory is not present 
    # Then create it.
    os.makedirs(folder+"output\\")
    outputFolder = folder+"output\\"
else:
    outputFolder = folder+"output\\"

# Get total items in folder and shuffle order
rangeCount = 0
for i in os.listdir(folder):
    if not i == 'output':
        rangeCount += 1
#str(input("Enter an inclusive Range in format #,#: "))
rangeArray = [0, rangeCount]
num = [i for i in range(int(rangeArray[0]),int(rangeArray[1]))]

if(GetShuffleImagesBool() == True):
    random.shuffle(num)

my_list = list(num)

ReoutputImages(outputFolder, folder, int(rangeArray[1]), my_list, imageName)
