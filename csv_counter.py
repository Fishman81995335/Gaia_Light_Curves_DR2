import io
import csv
import os
#
#
# Takes in name of csv file as a string without ".csv"
# Prints out number of separate sources in the csv
#
#


# Prompt name of file
fileName = str(input('enter csv file name: ')) + '.csv'
source_id = 0
num = 0

# Filter through individual file
# Filter through individual files
with open(fileName, 'r') as curves:
    reader = csv.reader(curves)
    lineNum = 0
    for line in reader:
        if not(line[0] == source_id) and not(lineNum == 0):
            num = num+1
            source_id = line[0]
        lineNum = lineNum + 1


message = "There are " + str(num) + " sources. \n"
print('\n')
print(message)
