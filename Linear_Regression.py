import csv
import shutil
import os
import numpy
#
#
# Takes directory in which results csv files are located
# creates new csv file that stores source ID's that match criteria
# Store linear regression values as well as RP and BP max/min ratio values
# Requires: source Id's in files are in ascending order with file names
# Requires: each source Id has at least one G band event
#
#
# TESTING
# '/Volumes/Untitled/Research/testing/Linear_Reg_Test_files/sifter_results/results'
# '/Volumes/Untitled/Research/testing/Linear_Reg_Test_files/sifter_results/BP_results'
# '/Volumes/Untitled/Research/testing/Linear_Reg_Test_files/sifter_results/RP_results'
# '/Volumes/Untitled/Research/testing/Lin_Reg_test_results'


# Calculate Files
dir = '/Volumes/Untitled/Research/Sifter_Results/sifter_results/results'
# str(input('\nEnter path to lin reg results folder: '))
# '/Volumes/Untitled/Research/Sifter_Results/sifter_results/results'
dir2 = '/Volumes/Untitled/Research/Sifter_Results/sifter_results/BP_results'
# str(input('\nEnter path to lin reg BP results folder: '))
# '/Volumes/Untitled/Research/Sifter_Results/sifter_results/BP_results'
dir3 = '/Volumes/Untitled/Research/Sifter_Results/sifter_results/RP_results'
# str(input('\nEnter path to lin reg RP results folder: '))
# '/Volumes/Untitled/Research/Sifter_Results/sifter_results/RP_results'
new_dir = '/Volumes/Untitled/Research/Linear_Regression_Results_squared'
# str(input('\nEnter path to folder where you want linear regression results: '))
# '/Volumes/Untitled/Research/Linear_Regression_Results_squared'
num_files = 0
print("\nCalculating total number of files...")
for fileName in os.listdir(dir):
    num_files = num_files+1
message = "There are " + str(num_files) + " files\n"
print(message)


source_id = 0


new_dir = new_dir+'/linear_regression_results'

try:
    shutil.rmtree(new_dir)
except:
    print('sifter folder created')

os.mkdir(new_dir)



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
for fileNum in range(1,num_files+1):
    print('processing file '+ str(fileNum) + ' \U0001f44d')
    # Get file from folder
    fileNameResult = dir + "/results_" + str(fileNum) + '.csv'
    newFileName = new_dir + "/results_" + str(fileNum) + '.csv'
    bp_file_name = dir2 + "/BP_results_" + str(fileNum) + '.csv'
    rp_file_name = dir3 + "/RP_results_" + str(fileNum) + '.csv'
    # Filter through individual file
    with open(fileNameResult, 'r') as result:
        with open(bp_file_name, 'r') as bp_file:
            with open(rp_file_name, 'r') as rp_file:
                with open(newFileName, 'w') as lin_reg_result:
                    reader = csv.reader(result)
                    bp_reader = csv.reader(bp_file)
                    rp_reader = csv.reader(rp_file)
                    writer = csv.writer(lin_reg_result)
                    line = next(reader)
                    lineSkip = 0
                    bp_line = next(bp_reader)
                    rp_line = next(rp_reader)
                    writer.writerow(['source_id', 'slope', 'intercept','R^2','BP_max/min','RP_max/min', 'count'])
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
                            bp_count = 0
                            rp_count = 0
                            # get bp array
                            while bp_line[0] != source_id:
                                bp_line = next(bp_reader)
                            bp = []
                            while bp_line[0] == source_id:
                                bp = bp + [float(bp_line[3])]
                                bp_count = bp_count + 1
                                try:
                                    bp_line = next(bp_reader)
                                except:
                                    break

                            # get rp array
                            while rp_line[0] != source_id:
                                rp_line = next(rp_reader)
                            rp = []
                            while rp_line[0] == source_id:
                                rp = rp + [float(rp_line[3])]
                                rp_count = rp_count + 1
                                try:
                                    rp_line = next(rp_reader)
                                except:
                                    break


                            rp_ratio = (numpy.amax(rp)/numpy.amin(rp))
                            bp_ratio = (numpy.amax(bp)/numpy.amin(bp))
                            
                            to_add = [source_id, numpy.polyfit(x, y, 1, w=weight)[0], numpy.polyfit(x, y, 1, w=weight)[1], \
                                    numpy.corrcoef(x,y)[0,1]**2, rp_ratio, bp_ratio, min([rp_count,bp_count])]
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
                                (numpy.corrcoef(x,y)[0,1]**2), rp_ratio, bp_ratio, min([rp_count,bp_count])]
                            writer.writerow(to_add)
                            break


print('\nSuccess! \U0001f600\n')
