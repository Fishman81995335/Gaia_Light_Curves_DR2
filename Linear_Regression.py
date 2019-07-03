import io
import csv
import urllib.request
import shutil
import os
import sys
import numpy
import statsmodels.formula.api as sm
import pandas as pd
import scipy
#
#
# Takes directory in which results csv files are located
# creates new csv file that stores source ID's that match criteria
# Store linear regression values
# Requires: source Id's in files are in ascending order with file names
# Requires: each source Id has at least one G band event
#
# Calculate Files
dir = str(input('\nEnter path to results folder: '))
new_dir = \
    str(input('\nEnter path to folder where you want linear regression results: '))
num_files = 0
print("\nCalculating total number of files...")
for fileName in os.listdir(dir):
    num_files = num_files+1
message = "There are " + str(num_files) + " files\n"
print(message)

# Iterate over rows to find number of source IDs
source_id = 0

new_dir = new_dir+'/linear_regression_results'

try:
    shutil.rmtree(new_dir)
except:
    print('sifter folder created')

os.mkdir(new_dir)

# use regular fit to compare with current algorithm
ols_fit = sm.ols

# returns [[slope, intercept]] of linear regression on a list of lists [array_list]
# Requires: list[n][1] is independent var and list[n][3] is dependent variable
# NOT USED IN MAIN FUNCTION


def lin_reg_a_b(array_list):
    counter = 0
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_x_sqrds = 0
    sum_y_sqrds = 0
    sum_x_sqrd = 0
    for line in array_list:
        counter = counter+1
        sum_x = sum_x + float(line[1])
        sum_y = sum_y + float(line[3])
        sum_xy = sum_xy + float(line[1])*float(line[3])
        sum_x_sqrds = sum_x_sqrds + float(line[1])**2
        sum_y_sqrds = sum_y_sqrds + float(line[3])**2
    sum_x_sqrd = sum_x**2

    return [(sum_y * sum_x_sqrds - sum_x * sum_xy) /
            (counter*sum_x_sqrds - sum_x_sqrd),
            (counter * sum_xy - sum_x * sum_y) /
            (counter * sum_x_sqrds - sum_x_sqrd)]


# Calculates weight and returns it for a given line
def wc(l): return (2/(float(l[8])-float(l[7])))**2


# Creates new files for each results file
for fileName in os.listdir(dir):
    print('processing file '+fileName + ' \U0001f44d')
    # Get file from folder
    fileNameResult = dir + "/" + fileName
    newFileName = new_dir + "/" + fileName
    # Filter through individual file

    with open(fileNameResult, 'r') as result:
        with open(newFileName, 'w') as lin_reg_result:
            reader = csv.reader(result)
            writer = csv.writer(lin_reg_result)
            line = next(reader)
            lineSkip = 0
            writer.writerow(['source_id', 'slope', 'intercept','R^2'])
            x = []
            y = []
            weight = []
            while True:
                # Case: Next line has same source and is of RP or BP Band
                # Events are added to RP and BP arrays that will later be recorded
                if (line[0] == source_id) and \
                        not(lineSkip == 0):
                    x.append(float(line[1]))
                    y.append(float(line[3]))
                    weight.append(wc(line))
                elif (lineSkip == 0):
                    lineSkip = lineSkip + 1
                elif (line[0] != source_id) and (x != []) and (y != []):
                    to_add = [source_id, numpy.polyfit(
                        x, y, 1, w=weight)[0], numpy.polyfit(x, y, 1, w=weight)[1]
                        ,numpy.corrcoef(x,y)]
                    source_id = line[0]
                    writer.writerow(to_add)
                    x = [float(line[1])]
                    y = [float(line[3])]
                    weight = [wc(line)]
                elif line[0] != source_id:
                    source_id = line[0]
                    x.append(float(line[1]))
                    y.append(float(line[3]))
                    weight.append(wc(line))
                try:
                    line = next(reader)
                except:
                    to_add = [source_id, numpy.polyfit(
                        x, y, 1, w=weight)[0], numpy.polyfit(x, y, 1, w=weight)[1],
                        numpy.corrcoef(x,y)]
                    writer.writerow(to_add)
                    break


print('\nSuccess! \U0001f600\n')
