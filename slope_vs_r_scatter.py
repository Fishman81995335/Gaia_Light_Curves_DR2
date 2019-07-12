import io
import csv
import shutil
import os
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')
import matplotlib.patches as mpatches
#
#
# Takes directory in which csv files of lin reg test results are located
# Takes in light curve data  directory  to csv files
# Takes in cut off parameters
# creates graphs for each light curve file and an aggregate master file
# For all light curves
#
# TESTING ONLY
# '/Volumes/Untitled/Research/testing/slope_r_plot_testing/lin_reg'
# '/Volumes/Untitled/Research/testing/slope_r_plot_testing/light_curves'
# '/Volumes/Untitled/Research/testing/slope_r_plot_testing/results'

directory = '/Volumes/Untitled/Research/Linear_Regression_Results_squared/linear_regression_results'
#str(input('\nEnter path to regression results folder: '))
#'/Volumes/Untitled/Research/Linear_Regression_Results_squared/linear_regression_results'
print('\U0001f44d')

dir3 = '/Volumes/Untitled/Research/light_curve_csv/src'
#str(input('\nEnter path to light curves folder: '))
#'/Volumes/Untitled/Research/light_curve_csv/src'
print('\U0001f44d')

new_dir = '/Volumes/Untitled/Research/slope_vs_r_plot'
#str(input('\nEnter path to folder where you want scatter plot: '))
#'/Volumes/Untitled/Research/slope_vs_r_plot'
print('\U0001f44d')

# input cutoffs
print('\nEnter cutoffs\n')
slope = .0025
#float(input('bp/rp slope cutoff: '))
r_s_min = 0
#float(input('middle r squared value: '))
flux_dev_1 = .3
#float(input('best flux ratio: '))
flux_dev_2 = .4
#float(input('good flux ratio: '))
flux_dev_3 = .5
#float(input('ok flux ratio: '))
min_count = 5
#float(input('minumum number of events: '))

flux_min_1 = 2 - flux_dev_1
flux_max_1 = 2 + flux_dev_1
flux_min_2 = 2 - flux_dev_2
flux_max_2 = 2 + flux_dev_2 
flux_min_3 = 2 - flux_dev_3
flux_max_3 = 2 + flux_dev_3 

num_files = 0
print("\nCalculating total number of files...")
for fileName in os.listdir(directory):
    num_files = num_files+1
message = "There are " + str(num_files) + " files\n"
print(message)

plot_dir = new_dir+'/plots'

shutil.rmtree(new_dir)
os.mkdir(new_dir)
os.mkdir(plot_dir)

master_file = new_dir + '/all_points.png'
skip_file = new_dir + '/skips.txt'
scatter_file = plot_dir+'/'
lin_file = directory + '/results_'


#create labels for graph:
red = 'RP_max/RP_min and BP_max/BP_min within ' + str(flux_dev_1) + ' of 2.'
blue = 'RP_max/RP_min and BP_max/BP_min within ' + str(flux_dev_2) + ' of 2.'
green = 'RP_max/RP_min and BP_max/BP_min within ' + str(flux_dev_3) + ' of 2.'
red_patch = mpatches.Patch(color='red', label=red)
blue_patch = mpatches.Patch(color='blue', label=blue)
green_patch = mpatches.Patch(color='green', label=green)

x_master = []
y_master = []
color_master = []
skip = open(skip_file, 'w')
for num in range(1,num_files+1):
    print('processing file '+ str(num) + ' \U0001f44d')
    x = []
    y = []
    color = []
    open_file = lin_file+str(num)+'.csv'
    curve_file = dir3 + '/' +str(num) + '.csv'
    with open(curve_file, 'r') as curve:
        with open(open_file, 'r') as result:
            file_reader = csv.reader(result)
            curve_reader = csv.reader(curve)
            for line in file_reader:
                if line[1] != 'slope':
                    bp_ratio = float(line[4])
                    rp_ratio = float(line[5])
                    count = float(line[6])

                    try:
                        if (bp_ratio > flux_min_1) and (bp_ratio < flux_max_1) \
                            and (rp_ratio > flux_min_1) and (rp_ratio < flux_max_1)\
                                and count>=min_count:
                            color = color + ['g']
                            x = x + [float(line[1])]
                            y = y + [float(line[3])]
                        elif (bp_ratio > flux_min_2) and (bp_ratio < flux_max_2) \
                            and (rp_ratio > flux_min_2) and (rp_ratio < flux_max_2)\
                                and count>=min_count:
                            color = color + ['b']
                            x = x + [float(line[1])]
                            y = y + [float(line[3])]
                        elif (bp_ratio > flux_min_3) and (bp_ratio < flux_max_3) \
                            and (rp_ratio > flux_min_3) and (rp_ratio < flux_max_3)\
                                and count>=min_count:
                            color = color + ['r']
                            x = x + [float(line[1])]
                            y = y + [float(line[3])]
                    except Exception as e:
                        print(e)
                        skip.write(line[0]+'\n')

    
    
    fig = plt.figure()
    axes = plt.gca()
    axes.set_xlim([-slope,slope])
    axes.set_ylim([r_s_min,1.1])
    plt.legend(handles=[red_patch,blue_patch,green_patch])
    for event in range(0,len(x)):
        if color[event] == "b":
            plt.scatter(x=x[event],y=y[event], c="blue", marker=">", s=1)
        elif color[event] == "r":
            plt.scatter(x=x[event],y=y[event], c="red", marker="*", s=1)
        else:
            plt.scatter(x=x[event],y=y[event], c="green", marker="o", s=1)
    plt.savefig(scatter_file+str(num)+'.png', dpi = 200)
    plt.close(fig)
    x_master = x_master + x
    y_master = y_master + y
    color_master = color_master + color

fig = plt.figure()
axes = plt.gca()
axes.set_xlim([-slope,slope])
axes.set_ylim([r_s_min,1.1])
plt.legend(handles=[red_patch,blue_patch,green_patch])

print('creating master file')
count = 0
for event in range(0, len(x_master)):
    if color_master[event] == "b":
        plt.scatter(x=x_master[event],y=y_master[event], c="blue", marker=">", s=.2)
    elif color_master[event] == "r":
        plt.scatter(x=x_master[event],y=y_master[event], c="red", marker="*", s=.2)
    else:
        plt.scatter(x=x_master[event],y=y_master[event], c="green", marker="o", s=.2)
    count = count +1
    if (count % 1000 == 0):
        print(str(count) + ' events have been processed')
plt.savefig(master_file, dpi = 300)
plt.close(fig)



print('\nSuccess! \U0001f600\n')
