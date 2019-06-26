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
#
#
fileName = str(input('enter text file name: ')) + '.txt'
lineList = [line.rstrip('\n') for line in open(fileName)]
dir = os.path.dirname(os.path.abspath(__file__))
print(lineList)
num = 0
source_id = 0

for link in range(len(lineList)):
  # Create new file with data from link
    newfile = dir + '/' + str(link) + '.csv'
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(lineList[link], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Filter through individual files
    with open(newfile,'r') as alerts:
      reader = csv.reader(alerts)
      for line in reader:
        if not(line[0] == source_id):
          num = num+1
          source_id = line[0]

    os.remove(newfilegz)
    os.remove(newfile)

print(num)