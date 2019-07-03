import io
import csv
import urllib.request
import shutil
import os
import sys
import numpy
#
#
# Takes directory in which csv files are
# creates 3 folders
# 1) Creates 'RP_results_n.csv' in 'RP_results' directory in 'sifter_results'
# directory with all RP events in nth file
# 2) Creates 'BP_results_n.csv' in 'BP_results' directory in 'sifter_results'
# directory with all BP events in nth file
# 3) Creates 'results_n.csv' in 'results' directory with the results of the
# events from the nth csv file. Filters results such that events that didn't
# have both BP and RP measurements at the same time are discarded.
# BP and RP files are written in following order without header:
# ['source_id','time','mag','flux','flux error']
# results files are written in following order with header:
# ['source_id','time','mag_BP_RP','flux_BP_RP','agg_flux_error']
# Requires: source Id's in files are in ascending order with file names
# Requires: each source Id has at least one G band event
#
#

# Calculate Files
dir = str(input('\nEnter path to source folder: '))
new_dir = str(input('\nEnter path to folder where you want results: '))
code_dir = os.path.dirname(os.path.realpath(__file__))
num_files = 0
print("\nCalculating total number of files...")
for fileName in os.listdir(dir):
    num_files = num_files+1


message = "There are " + str(num_files) + " files\n"
print(message)

# Initialize Source ID
source_id = 0

# Create new directories for new files
folder = new_dir+'/sifter_results'

try:
    shutil.rmtree(folder)
except:
    print('sifter folder created')

os.mkdir(folder)
os.mkdir(new_dir+'/sifter_results'+'/results')
os.mkdir(new_dir+'/sifter_results'+'/BP_results')
os.mkdir(new_dir+'/sifter_results'+'/RP_results')


# Creates new files for each gaia database file and enters results
for fileName in os.listdir(dir):
    print('processing file '+fileName + ' \U0001f44d')
    # Get file from folder
    newFileName = dir + "/" + fileName
    # Filter through individual file

    with open(newFileName, 'r') as curve2:
        reader = csv.reader(curve2)
        lineSkip = 0
        line = next(reader)
        RP_array = []
        BP_array = []
        RP_lin_array = []
        BP_lin_array = []
        while True:
            # Case: Next line has same source and is of RP or BP Band
            # Events are added to RP and BP arrays that will later be recorded
            if (line[0] == source_id) and \
                    not(lineSkip == 0):
                if (str(line[2]) == 'RP'):
                    to_add = []
                    to_add.append(line[0])
                    to_add.append(line[3])
                    to_add.append(line[4])
                    to_add.append(line[5])
                    to_add.append(line[6])
                    RP_lin_array.append(to_add)
                elif(str(line[2]) == 'BP'):
                    to_add = []
                    to_add.append(line[0])
                    to_add.append(line[3])
                    to_add.append(line[4])
                    to_add.append(line[5])
                    to_add.append(line[6])
                    BP_lin_array.append(to_add)
            # Case: Header line (we want to ignore this)
            elif (lineSkip == 0):
                lineSkip = lineSkip + 1
            # Case: New Source_ID is found so arrays are recorded
            elif (line[0] != source_id) and (RP_lin_array != []) and \
                    (BP_lin_array != []):
                source_id = line[0]
                RP_array.append(RP_lin_array)
                RP_lin_array = []
                BP_array.append(BP_lin_array)
                BP_lin_array = []
            # First line case when no RP is recorded but source_ID 
            # is also different
            elif line[0] != source_id:
                source_id = line[0]
            try:
                line = next(reader)
            except:
                RP_array.append(RP_lin_array)
                BP_array.append(BP_lin_array)
                break

    assert(len(BP_array) == len(RP_array))

    # filter through both arrays
    # Open files for BP and RP Results
    # These files will then be read to filter through for the final results file
    with open(new_dir+'/sifter_results'+'/BP_results'+'/BP_results_' + fileName, 'w') as BP_file:
        BP_writer = csv.writer(BP_file)
        for n in range(len(BP_array)):
            for m in range(len(BP_array[n])):
                BP_writer.writerow(BP_array[n][m])

    with open(new_dir+'/sifter_results'+'/RP_results'+'/RP_results_' + fileName, 'w') as RP_file:
        RP_writer = csv.writer(RP_file)
        for n in range(len(RP_array)):
            for m in range(len(RP_array[n])):
                RP_writer.writerow(RP_array[n][m])

    # open writer for results file
    with open((new_dir+'/sifter_results'+'/results'+'/results_' + fileName), 'w') as to_write:
        # write headers
        writer = csv.writer(to_write)
        writer.writerow(['source_id', 'time', 'mag_BP_RP',
                         'flux_BP/RP', 'BP_flux_error', 'RP_flux_error', 'agg_flux_error', 'flux_BP/RP_lower', 'flux_BP/RP_upper'])

        # Sift through and remove points that don't have counterparts
        BP_s_counter = 0
        RP_s_counter = 0
        BP_v_counter = 0
        RP_v_counter = 0
        while (BP_s_counter < len(BP_array) and RP_s_counter < len(RP_array)):
            while (BP_v_counter < len(BP_array[BP_s_counter])) and \
                    (RP_v_counter < len(RP_array[RP_s_counter])):
                # Cases: RP and BP times of event don't match within .02
                # Increment lower of two and keep comparing
                if float(RP_array[RP_s_counter][RP_v_counter][1]) - float(BP_array[BP_s_counter][BP_v_counter][1]) > .02:
                    BP_v_counter = BP_v_counter + 1
                elif float(RP_array[RP_s_counter][RP_v_counter][1]) - float(BP_array[BP_s_counter][BP_v_counter][1]) < -.02:
                    RP_v_counter = RP_v_counter + 1
                # Times of RP and BP events match within .02. Record Event in 
                # results file.
                # See header above for entries
                else:
                    newEntry = []
                    newEntry.append(RP_array[RP_s_counter][RP_v_counter][0])
                    newEntry.append((float(RP_array[RP_s_counter][RP_v_counter][1]) +
                                     float(BP_array[BP_s_counter][BP_v_counter][1]))/2)
                    newEntry.append(
                        (float(BP_array[BP_s_counter][BP_v_counter][2]))-(float(RP_array[RP_s_counter][RP_v_counter][2])))
                    newEntry.append(
                        (float(BP_array[BP_s_counter][BP_v_counter][3]))/(float(RP_array[RP_s_counter][RP_v_counter][3])))
                    newEntry.append(BP_array[BP_s_counter][BP_v_counter][4])
                    newEntry.append(RP_array[RP_s_counter][RP_v_counter][4])
                    newEntry.append(numpy.sqrt(
                        (float(RP_array[RP_s_counter][RP_v_counter][4])**2) + (float(BP_array[BP_s_counter][BP_v_counter][4])**2)))
                    newEntry.append((float(BP_array[BP_s_counter][BP_v_counter][3]) - float(BP_array[BP_s_counter][BP_v_counter][4]))
                                    / (float(RP_array[RP_s_counter][RP_v_counter][3]) + float(RP_array[RP_s_counter][RP_v_counter][4])))
                    newEntry.append((float(BP_array[BP_s_counter][BP_v_counter][3]) + float(BP_array[BP_s_counter][BP_v_counter][4]))
                                    / (float(RP_array[RP_s_counter][RP_v_counter][3]) - float(RP_array[RP_s_counter][RP_v_counter][4])))
                    
                    writer.writerow(newEntry)
                    RP_v_counter = RP_v_counter + 1
                    BP_v_counter = BP_v_counter + 1

            RP_s_counter = RP_s_counter + 1
            BP_s_counter = BP_s_counter + 1
            RP_v_counter = 0
            BP_v_counter = 0

print('\nSuccess! \U0001f600\n')
