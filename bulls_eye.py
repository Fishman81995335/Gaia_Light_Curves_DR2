import os
import shutil
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import csv
#
#
# Takes in directory to linear regression results csv files
# Takes in directory to light curve files
# Creates 3 plots
# 1) bullseye for 2 - mag vs 1 - r squared
# 2) bullseye for 2 - mag vs slope
# 3) bullseye for 1 - r squared vs slope
#
#
lin_reg_dir = '/Volumes/Untitled/Research/Linear_Regression_Results_squared/linear_regression_results'
# str(input('\nEnter path to event lin reg results folder: '))
results_dir = '/Volumes/Untitled/Research/Bulls_eye'
# str(input('\nEnter path to results file: '))

slope_cut = .0025
# str(input('\nInput slope cut off: '))
r_cut = .8
# str(input('\nInput r squared cut off: '))
ratio_tol = .4
# str(input('\nInput the tolerance on max/min flux ratio from 2: '))
tol_up = 2+.4
tol_down = 2-.4
num_events = 5
# int(input('\nInput min number of bp rp events per source id'))
n = 15
# int(input('\nInput how many top values you'd like in text file))

x = []
y = []
z = []
goodness = []
point = []
count = 0
source = []
for filename in os.listdir(lin_reg_dir):
  print('processing file ' + str(filename) + ' \U0001f44d')
  file_dir = lin_reg_dir + '/' + filename
  with open(file_dir, 'r') as lin_reg:
    file_reader = csv.reader(lin_reg)
    for line in file_reader:
      if line[0] != 'source_id':
        if abs(float(line[1]))< slope_cut and float(line[3]) > r_cut and \
          float(line[4]) < tol_up and float(line[4]) > tol_down and \
            float(line[5]) < tol_up and float(line[5]) > tol_down and \
              num_events <= int(line[6]):
            source = source + [str(line[0])]
            x = x + [float(line[1])]
            y = y + [1 - float(line[3])]
            bp_rat = float(line[4])
            rp_rat = float(line[5])
            rat = np.amax([bp_rat, rp_rat])
            z = z + [2 - rat]
            goodness = goodness + [(float(line[1])**2 + (1 - float(line[3]))**2 + (2-rat)**2)]
            count = count + 1

new_good = sorted(goodness, reverse=False)
best = new_good[:n]

print('There are ' + str(count) + ' events to plot')
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim(0,slope_cut)
ax.set_ylim(0,1-r_cut)
ax.set_zlim(0,ratio_tol)
ax.set_xlabel('slope')
ax.set_ylabel('1 - r^2')
ax.set_zlabel('2 - max/min flux ratio')
file_dir = results_dir + '/results.txt'
writer = open(file_dir, 'w')
for event in range(0,count):
  if goodness[event] in best:
    ax.scatter3D(x[event],y[event],z[event],c='g',s=2)
    writer.write(source[event]+'\n')
  else:
    ax.scatter3D(x[event],y[event],z[event],c='b',s=2)
plt.show()
plt.close(fig)


