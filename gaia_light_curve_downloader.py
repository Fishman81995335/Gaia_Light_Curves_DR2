import csv
import urllib.request
import os
import gzip
import shutil
#
#
# Takes in string as name of new folder in which files will be stored.
# Unzips and returns csv files in folder with the name entered.
# Folder will be created in the directory of the location of the python code
# Files inside folder will be named 0 to x for the x files in gaia database
# Text file provided in this repository is named "file_links"
#
#

fileName = str(input('enter text file name: ')) + '.txt'
url = [line.rstrip('\n') for line in open(fileName)]

dir = str(input('enter folder path: '))

print("Calculating total number of files...")
num_files = len(url)
if num_files == 1:
    print("There is 1 file")
else:
    message = "There are " + str(num_files) + " files"
    print(message)

for x in range(len(url)):
    message = "downloading file number " + \
        str(x+1) + " out of " + str(num_files)
    print(message)
    newfile = dir + '/' + str(x) + '.csv'
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(url[x], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(newfilegz)
print('\nsuccess!\n')