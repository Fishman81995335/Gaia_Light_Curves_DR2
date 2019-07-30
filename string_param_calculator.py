import numpy as np
import csv
#
#
# Takes in csv file with data about string
# Takes in user input of microlensing event length
# returns range of string tensions and mean in csv file
#
#
dr2_file = '/Users/vineetkamat/Desktop/Results/DATA/dr2 data-result.csv'
#str(input('Input full path name of csv file with dr2 results: '))
print('\n\U0001f44d\n')
new_dir = '/Users/vineetkamat/Desktop/Results/DATA/string_results'
#str(input('Input the directory of results file: '))
print('\n\U0001f44d\n')
new_file = new_dir + '/tensions.csv'
print('\n\U0001f44d\n')

# conversion factor to convert julian date to seconds and 1/parallax to kilometers
conv_fact_1 = float(86400)/(3.086*(10**13))
# only converts 1/parallax to km
conv_fact_2 = float(1/(3.086*(10**13)))

with open(dr2_file, 'r') as dr2:
  with open(new_file, 'w') as nf:
    nf_write = csv.writer(nf)
    nf_write.writerow(['source_id','tension high','tension low'])
    dr2_reader = csv.reader(dr2)
    for line in dr2_reader:
      if str(line[2]) == 'source_id':
        continue
      tf = int(input('Input 1 if light curve '+str(line[2])+' has a 1 point peak and 2 if more: '))
      if tf == 1:
        t1 = float(input('Enter time of microlensing event ' + str(line[2]) +' in JD: '))
        # ten_high = str_velocity * (par + par_err) * time_interval / (root(2)pi)
        ten_high = float(299792) * (abs(float(line[9]))+abs(float(line[10]))) * t1 * conv_fact_1 \
          /(np.pi*np.sqrt(2))
        ten_low = float(299792) * (4.4) * (abs(float(line[9]))+abs(float(line[10]))) * conv_fact_2 \
          /(np.pi*np.sqrt(2))

        rat = ten_high/ten_low
        sc = str(line[2])
        print('sourcgfgffffgffse_ID: '+ str(sc))
        print('tension high cutoff: ' + str(ten_high))
        print('tension low cutoff: ' + str(ten_low))
        print(rat)
        print(rat*4.4/(86400))
        print(t1*86400/4.4)
        nf_write.writerow([sc,ten_high,ten_low])
      elif tf == 2:
        continue

    nf.close()
  dr2.close()