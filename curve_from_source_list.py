import os
import csv
import shutil
import matplotlib.pyplot as plt

#
# Takes in text file with source ID's
# Takes in string of directory to light curves
# Takes in string of directory to where you want new curves
# Retrieves light curves of each source as 'source_ID'.csv
#
#
light_curve_dir = '/Volumes/Untitled/Research/light_curve_csv/src'
# str(input('Light curve directory: ))
# '/Volumes/Untitled/Research/light_curve_csv/src'
id_file_dir = '/Volumes/Untitled/Research/Bulls_eye/results.txt'
# '/Volumes/Untitled/Research/testing/curve_from_source_test_files/results.txt'
#'/Volumes/Untitled/Research/Bulls_eye/results.txt'
# str(input('Source ID file full pathname with .txt: '))
new_dir = '/Volumes/Untitled/Research/curves_from_source_list'
# str(input('Folder for light curve and plot outputs'))

shutil.rmtree(new_dir)
os.mkdir(new_dir)

f = open(id_file_dir, 'r')
def dat_fun():
    with open(id_file_dir, "r") as ifile:
      source_array = []
      for line in ifile:
        line = line.split('\n')
        if str(line[0]) != '':
          source_array = source_array + [str(line[0])]
    ifile.close()
    return source_array


def read_file(element, num):
  csv_dir = light_curve_dir + '/' + str(num) +'.csv'
  with open(csv_dir,'r') as f:
    fr = csv.reader(f)
    line = next(fr)
    while str(line[0]) != element:
      try:
        line = next(fr)
      except:
        num = num + 1
        return read_file(element, num)
    array = []
    while str(line[0]) == element:
      array = array + [line]
      line = next(fr)
    return [num,array]

source_array = dat_fun()
source_array.sort(reverse=False)

main = []
num = 1
for count in range(0,len(source_array)):
  print('processing source ' + str(source_array[count]))
  array = read_file(source_array[count],num)
  main = main + [array[1]]
  num = array[0]

csv_dir = new_dir + '/csv_files'
os.mkdir(csv_dir)

plot_dir = new_dir + '/plots'
os.mkdir(plot_dir)

print('writing csv and plot files... ')


for line in main:
  print('working on file ' + str(line[0][0]) + ' \U0001f44d')
  csv_file_dir = csv_dir + '/' + str(line[0][0]) + '.csv'
  fig_dir = plot_dir + '/' + str(line[0][0]) + '.png'
  fig = plt.figure()
  rp_t = []
  bp_t = []
  rp_val = []
  bp_val = []
  rp_err = []
  bp_err = []
  with open(csv_file_dir, 'w') as csvf:
    csv_writer = csv.writer(csvf)
    for event in line:
      csv_writer.writerow(event)
      if str(event[2]) == 'BP':
        bp_t = bp_t + [float(event[3])]
        bp_val = bp_val + [float(event[5])]
        bp_err = bp_err + [float(event[6])]
      elif str(event[2]) == 'RP':
        rp_t = rp_t + [float(event[3])]
        rp_val = rp_val + [float(event[5])]
        rp_err = rp_err + [float(event[6])]
  csvf.close()
  plt.errorbar(x=bp_t, y=bp_val, yerr=bp_err, fmt='b-o', capsize=3)
  plt.errorbar(x=rp_t, y=rp_val, yerr=rp_err, fmt='r-o', capsize=3)
  plt.savefig(fig_dir, dpi = 400)
  plt.close(fig)

