import io
import csv
import shutil
import os
import numpy
import matplotlib.pyplot as plt
#
#
# Takes directory in which results csv files are located
# Creates new csv files that store source ID's that match criteria
# Create plots for each of these source ID's
# Requires: source Id's in files are in ascending order with file names
# Requires: source Id's in both regression results and light curves files are
# in same order and same source Id's are in both
# Requires: Names of files are the same as assigned by gaia_downloader file
#
# Calculate Files
directory = '/Volumes/Untitled/Research/testing/Lin_Reg_test_results/linear_regression_results'
# str(input('\nEnter path to regression results folder: '))
print('\U0001f44d')
dir2 = '/Volumes/Untitled/Research/testing/Linear_Reg_Test_files/sifter_results/results'
# str(input('\nEnter path to event sifter results folder: '))
print('\U0001f44d')
dir3 = '/Volumes/Untitled/Research/testing/light_curves_test'
# str(input('\nEnter path to light curves folder: '))
print('\U0001f44d')
new_dir = \
    '/Volumes/Untitled/Research/testing/Achrom_testing'
    # str(input('\nEnter path to folder where you want achromatic sifter files: '))
print('\U0001f44d')

num_files = 0


print("\nCalculating total number of files...")
for fileName in os.listdir(directory):
    num_files = num_files+1
message = "There are " + str(num_files) + " files\n"
print(message)


new_dir2 = new_dir+'/achromatic_sifter_plots'
new_dir3 = new_dir+'/achromatic_sifter_results'

shutil.rmtree(new_dir)
os.mkdir(new_dir)

os.mkdir(new_dir2)
print('achromatic plot folder created')
os.mkdir(new_dir3)
print('achromatic results folder created')




# Create one new files for all results
newFileName = new_dir3 + "/" + 'achromatic_sifter_results.csv'
with open(newFileName, 'w') as achrom_result:
    writer = csv.writer(achrom_result)
    writer.writerow(['source_id', 'slope', 'intercept', 'R^2'])
    light_curve_number = 0
    for fileName in os.listdir(directory):
        light_curve_number = light_curve_number + 1
        curve_file = dir2 + '/results_' + str(light_curve_number) + '.csv'
        print('processing file '+fileName + ' \U0001f44d')
        # Get file from folder
        fileNameResult = directory + "/" + fileName
        # Filter through individual file
        with open(fileNameResult, 'r') as result:
            with open(curve_file, 'r') as curve:
                reader1 = csv.reader(result)
                reader2 = csv.reader(curve_file)
                # Read once to get rid of header
                line = next(reader1)
                line2 = next(reader2)
                print(line2)
                for line in reader1:
                    x = []
                    y = []
                    y_err = []
                    try:
                        if abs(float(line[1])) < .2 and (float(line[3]) > .8):
                            writer.writerow(line)
                            while line2[0] != line[0]:
                                print('lol1')
                                line2 = reader2.next()
                                print('lol2')
                            while line2[0] == line[0]:
                                x.append(float(line2[1]))
                                y.append(float(line2[3]))
                                y_err.append((float(line[8])-float(line[7]))/2)
                            plt.figure()
                            plt.errorbar(x,y,yerr = y_err,barsabove = True)
                            plt.savefig(new_dir2)


                    except:
                        print('line skipped')


print('\nSuccess! \U0001f600\n')
