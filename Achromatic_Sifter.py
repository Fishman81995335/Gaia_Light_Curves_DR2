import io
import csv
import shutil
import os
import numpy
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import matplotlib.patches as mpatches
#
#
# Takes string of directory in which results csv files are located for lin reg,
# and event sifter, and directory for light curves
# Takes in numbers for slope, r squared, max and min flux ratios, and min
# number of events
# Creates new csv files that store source ID's that match criteria
# Create plots for each of these source ID's
# Requires: source Id's in files are in ascending order with file names
# Requires: source Id's in both regression results and light curves files are
# in same order and same source Id's are in both
# Requires: Names of files are the same as assigned by gaia_downloader file
#
#
# TESTING:
# /Volumes/Untitled/Research/testing/Achrom_testing/last source test/lin_results
# /Volumes/Untitled/Research/testing/Achrom_testing/last source test/sifter
# /Volumes/Untitled/Research/testing/Achrom_testing/last source test/light_curve
# /Volumes/Untitled/Research/testing/Achrom_testing/last source test/Achrom

directory = '/Volumes/Untitled/Research/Linear_Regression_Results_squared/linear_regression_results'
#str(input('\nEnter path to regression results folder: '))
#'/Volumes/Untitled/Research/testing/Lin_Reg_test_results/linear_regression_results'
#'/Volumes/Untitled/Research/Linear_Regression_Results_squared/linear_regression_results'
print('\U0001f44d')

dir2 = '/Volumes/Untitled/Research/Sifter_Results/sifter_results/results'
#str(input('\nEnter path to event sifter results folder: '))
#'/Volumes/Untitled/Research/testing/Linear_Reg_Test_files/sifter_results/results'
#'/Volumes/Untitled/Research/Sifter_Results/sifter_results/results'
print('\U0001f44d')

dir3 = '/Volumes/Untitled/Research/light_curve_csv/src'
#str(input('\nEnter path to light curves folder: '))
#'/Volumes/Untitled/Research/testing/light_curves_test'
#'/Volumes/Untitled/Research/light_curve_csv/src'
print('\U0001f44d')

new_dir = str(input('\nEnter path to folder where you want achromatic sifter files: '))
#'/Volumes/Untitled/Research/testing/Achrom_testing'
#'/Volumes/Untitled/Research/Achromatic/Achrom_Sifter_squared'
#'/Volumes/Untitled/Research/Achromatic/Achrom_Squared_flux_dif'
print('\U0001f44d')

# input cutoffs
print('\nEnter cutoffs\n')
slope = float(input('bp/rp slope cutoff: '))
r_s_min = float(input('mininum r squared value: '))
flux_min = float(input('minimum flux ratio: '))
flux_max = float(input('maximum flux ratio: '))
min_count = float(input('minumum number of events: '))

num_files = 0


print("\nCalculating total number of files...")
for fileName in os.listdir(directory):
    num_files = num_files+1
message = "There are " + str(num_files) + " files\n"
print(message)


new_dir2 = new_dir+'/achromatic_sifter_plots'
new_dir3 = new_dir+'/achromatic_sifter_results'
new_dir4 = new_dir+'/light_curves'

shutil.rmtree(new_dir)
os.mkdir(new_dir)

os.mkdir(new_dir2)
print('achromatic plot folder created')
os.mkdir(new_dir3)
print('achromatic results folder created')
os.mkdir(new_dir4)
print('ligth curve folder created')


#create labels for graph:
red = 'RP band light curve'
blue = 'BP band light curve'
red_patch = mpatches.Patch(color='red', label=red)
blue_patch = mpatches.Patch(color='blue', label=blue)


# Create one new files for all results
newFileName = new_dir3 + "/" + 'achromatic_sifter_results.csv'
with open(newFileName, 'w') as achrom_result:
    writer = csv.writer(achrom_result)
    writer.writerow(['source_id', 'slope', 'intercept', 'R^2'])
    light_curve_number = 0
    for light_curve_number in range(1,num_files+1):
        # Get sifted events file from folter
        sifter_file = dir2 + '/results_' + str(light_curve_number) + '.csv'
        print('processing file '+ str(light_curve_number) + ' \U0001f44d')
        # Get result file from folder
        fileNameResult = directory + '/results_' + str(light_curve_number) + '.csv'
        # Get light curve file from folder
        curve_file = dir3 + '/' +str(light_curve_number) + '.csv'
        # Filter through individual file
        with open(fileNameResult, 'r') as result:
            with open(sifter_file, 'r') as sifter:
                with open(curve_file, 'r') as curve:

                    #make readers
                    reader1 = csv.reader(result)
                    reader2 = csv.reader(sifter)
                    reader3 = csv.reader(curve)

                    # Read once to get rid of header for reader 1
                    # Read twice for reader 2 and 3
                    line = next(reader1)
                    line2 = next(reader2)
                    line2 = next(reader2)
                    line3 = next(reader3)
                    line3 = next(reader3)
                    

                    for line in reader1:
                        x = []
                        y = []
                        y_err = []
                        try:
                            if abs(float(line[1])) <= slope and (float(line[3]) >= r_s_min):
                                # get next line while line is not of source_id
                                while line3[0] != line[0]:
                                    line3 = next(reader3)
                                # Append values from light curve file until source_id changes
                                bp_t = []
                                rp_t = []
                                bp_val = []
                                rp_val = []
                                bp_err = []
                                rp_err = []
                                while line3[0] == line[0]:
                                    if str(line3[2]) == 'BP':
                                        bp_t.append(float(line3[3]))
                                        bp_val.append(float(line3[5]))
                                        bp_err.append(float(line3[6]))
                                    elif str(line3[2]) == 'RP':
                                        rp_t.append(float(line3[3]))
                                        rp_val.append(float(line3[5]))
                                        rp_err.append(float(line3[6]))
                                    try:
                                        line3 = next(reader3)
                                    except:
                                        break
                                
                                if (max(bp_val) > flux_min*min(bp_val)) and (max(bp_val) < flux_max*min(bp_val)) \
                                    and (max(rp_val) > flux_min*min(rp_val)) and (max(rp_val) < flux_max*min(rp_val)):


                                    # get next line while line is not of source_id
                                    while line2[0] != line[0]:
                                        line2 = next(reader2)

                                    # Append values from sifted file source_id changes
                                    count = 0
                                    while line2[0] == line[0]:
                                        x.append(float(line2[1]))
                                        y.append(float(line2[3]))
                                        y_err.append((float(line2[8])-float(line2[7]))/2)
                                        count = count + 1
                                        try:
                                            line2 = next(reader2)
                                        except:
                                            break
                                    # Check if error bars contain best fit line
                                    in_range = True
                                    for event in range(0,len(x)):
                                        val = (x[event]*float(line[1]) + float(line[2]))
                                        in_range = in_range and \
                                            ((y_err[event] + y[event]) > val) and\
                                                ((y[event] - y_err[event]) < val)

                                    if (count >= min_count) and in_range:

                                        #create info:
                                        info = 'bp ratio: ' + str(line[4]) + ' ' + \
                                            'rp ratio: ' + str(line[5]) + '\n' + \
                                                'r^2: ' + str(line[3]) + ' ' + \
                                                    'slope: ' + str(line[1]) + '\n' + \
                                                        'count: ' + str(count)

                                        val1 = x[0]*float(line[1]) + float(line[2])
                                        val2 = val
                                        # plot bp/rp
                                        fig = plt.figure()
                                        plt.plot([x[0], x[count-1]],[val1, val2])
                                        plt.errorbar(x,y,fmt = 'r^', elinewidth=1,yerr = y_err,barsabove = True, capsize=3)
                                        plt.ylabel('flux bp/rp')
                                        plt.xlabel('time')
                                        plt.savefig(new_dir2+'/'+'achromatic_'+str(line[0])+'.png')
                                        plt.close(fig)
                                        # plot bp rp light curve
                                        fig2 = plt.figure()
                                        plt.errorbar(x=bp_t, y=bp_val, yerr=bp_err, fmt='b-o', capsize=3)
                                        plt.errorbar(x=rp_t, y=rp_val, yerr=rp_err, fmt='r-o', capsize=3)
                                        plt.legend(handles=[red_patch,blue_patch])
                                        plt.title(str(line[0]))
                                        plt.ylabel('flux')
                                        plt.xlabel('time')
                                        plt.figtext(.7,.95, 'bp ratio: ' + str(line[4]))
                                        plt.figtext(.05,.95, 'rp ratio: ' + str(line[5]))
                                        plt.figtext(.7,.9, 'r^2: ' + str(line[3]))
                                        plt.figtext(.05,.9, 'count: ' + str(count))
                                        plt.savefig(new_dir4+'/'+'time_series_'+str(line[0])+'.png', dpi = 300)
                                        plt.close(fig2)
                                        writer.writerow(line)


                        except Exception as e:
                            print(e)
                            print('line skipped')

read_me_dir = new_dir + '/README.txt'
print('writing readme...')
readme = open(file = read_me_dir, mode= 'w')
readme.write('Minimum counts is ' + str(min_count))
readme.write('\nAbsolute value of slope less than or equal to '+str(slope))
readme.write('\nR squared value is at least '+str(r_s_min))
readme.write('\nRatio of Maximum to Minimum RP and BP fluxes are between '\
    + str(flux_min) + ' and ' + str(flux_max))




print('\nSuccess! \U0001f600\n')
