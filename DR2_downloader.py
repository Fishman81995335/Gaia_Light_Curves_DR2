import os
import shutil
import csv
import gzip
import urllib.request
#
#
#
# Takes in path to dr2 download file links txt file
# named "DR2_links.txt" in this repository
# Downloads DR2 in text files numbered from 1 to n for n number of files in text file
# Downloaded files are in .csv format
#
#
links = str(input("Enter pathname of text file with '.txt': "))
print('\n\U0001f44d\n')
dir = str(input("Enter directory where you would like your csv files. Directory will first be deleted: "))
print('\n\U0001f44d\n')
url = [line.rstrip('\n') for line in open(links)]
link_count = 0
for link in url:
  link_count = link_count + 1

print("There are " + str(link_count) + " sources! \U0001f600")


shutil.rmtree(dir)
os.mkdir(dir)
print("New directory made \U0001f600")

count = 1
for file_url in url:
  print("processing file number "+str(count)+ " \U0001F608")
  newfile = dir + '/' + str(count) + '.csv'
  newfilegz = newfile + '.gz'
  urllib.request.urlretrieve(file_url, newfilegz)
  with gzip.open(newfilegz, 'rb') as f_in:
      with open(newfile, 'wb') as f_out:
          shutil.copyfileobj(f_in, f_out)
  os.remove(newfilegz)
  count = count+1

print('\nSuccess! \U0001f600\n')