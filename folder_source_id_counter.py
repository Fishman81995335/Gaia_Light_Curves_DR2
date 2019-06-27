import io
import csv
import urllib.request
import shutil
import gzip
import os, sys
#
#
# Takes in name of the links text file as a string without ".txt"
# Prints out number of separate sources in the different files
# Requires that source_id is a non zero integer and that source_id's are inputed
# in ascending order
#
dir = str(input('enter path to folder: '))
num = 0
source_id = 0
num_files = 0

print("Calculating total number of files...")
for fileName in os.listdir(dir):
    num_files = num_files+1
    print(fileName)
message = "There are " + str(num_files) + " files"
print(message)


counter = 1
for fileName in os.listdir(dir):
  # Get file from folder
    message = "processing file number " + \
        str(counter) + " out of " + str(num_files)
    print(message)

    newFileName = dir + "/" + fileName
    # Filter through individual file
    with open(newFileName, 'r') as curve:
        reader = csv.reader(curve)
        lineNum = 0
        for line in reader:
            if not(line[0] == source_id) and not(lineNum == 0):
                num = num+1
                source_id = line[0]
            if (lineNum == 0):
                lineNum = lineNum + 1

    counter = counter+1
message = "There are " + str(num) + " sources. \n"
print('\n')
print(message)
