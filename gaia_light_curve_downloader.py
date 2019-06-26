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
print(url)

newfolder = str(input('enter new folder name: '))
dir = os.path.dirname(os.path.abspath(__file__)) + '/' + newfolder
os.mkdir(dir)


for x in range(len(url)):
    newfile = dir + '/' + str(x) + '.csv'
    print(newfile)
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(url[x], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(newfilegz)
