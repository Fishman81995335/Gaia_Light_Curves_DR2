import io
import csv
import urllib.request
import shutil
import gzip
import os
#
#
# Takes in name of the links text file as a string without ".txt"
# Prints out number of separate sources in the different files
# Requires that source_id is a non zero integer and each source has a unique
# source id
#
fileName = str(input('enter text file name: ')) + '.txt'
lineList = [line.rstrip('\n') for line in open(fileName)]
dir = os.path.dirname(os.path.abspath(__file__))
num = 0
source_id = 0

print("Calculating total number of files...")
num_files = len(lineList)
message = "There are " + str(num_files) + " files"
print(message)

for link in range(len(lineList)):
  # Create new file with data from link
    newfile = dir + '/' + str(link) + '.csv'
    newfilegz = newfile + '.gz'
    message = "processing file number " + \
        str(link+1) + " out of " + str(num_files)
    print(message)
    urllib.request.urlretrieve(lineList[link], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Filter through individual files
    with open(newfile, 'r') as curves:
        reader = csv.reader(curves)
        lineNum = 0
        for line in reader:
            if not(line[0] == source_id) and not(lineNum == 0):
                num = num+1
                source_id = line[0]
            if (lineNum == 0):
                lineNum = lineNum + 1

    os.remove(newfilegz)
    os.remove(newfile)
message = "There are " + str(num) + " sources. \n"
print('\n')
print(message)
