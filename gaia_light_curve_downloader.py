import csv
import urllib.request
import os
import gzip
import shutil
#
#
# Takes in 2 strings on prompt
# First string is name of text file (without '.txt') in which links of urls
# are stored. Text file provided in repository is 'file_links.txt'
# Second string is path of new folder in which files will be stored
# WARNING: Contents of folder will be deleted
# Unzips and returns csv files in 2 folder, src and var.
# Folder will be created in the directory of the location of the python code
# Files inside folder will be named 0 to x for the x files in gaia database
# Text file provided in this repository is named "file_links"
#
#

fileName = str(input('enter text file name: ')) + '.txt'
url = [line.rstrip('\n') for line in open(fileName)]

print("Please ensure folder is emtpy. All contents will be deleted.")
dir = str(input('enter folder path: '))

# Get path names
dir_main = dir
dir2 = dir + '/var'
dir = dir + '/src'

# Delete current directory
for the_file in os.listdir(dir_main):
    file_path = os.path.join(dir_main, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

# Make directories
os.mkdir(dir)
os.mkdir(dir2)
print("\nPaths created\n")


# Calculate number of files for source and variability data
print("Calculating total number of files...")
num_lines = len(url)
n = 0
while url[n] != 'source_data':
    n = n+1


num_var_files = n-1
num_source_files = len(url) - 2 - num_var_files

# Print number of files
message = "There are " + str(num_lines-2) + " files\nThere are " + \
    str(num_var_files) + " variability data files and " + \
    str(num_source_files) + " source files! \U0001f44d"
print(message)


print('\nDownloading variability files...')


for x in range(num_var_files):
    message = "Downloading var file number " + \
        str(x+1) + " out of " + str(num_var_files) + ' \U0001f44d'
    print(message)
    newfile = dir2 + '/' + str(x+1) + '.csv'
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(url[x+1], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(newfilegz)


print('\nVariability file downloaded! \U0001f600\n')
print('\nDownloading source files...\n')

for x in range(num_source_files):
    y = x + num_var_files
    message = "Downloading source file number " + \
        str(x+1) + " out of " + str(num_source_files) + ' \U0001f44d'
    print(message)
    newfile = dir + '/' + str(x+1) + '.csv'
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(url[y+2], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(newfilegz)

print('\nSource Files Downloaded! \U0001f600\n')


print('\nSuccess! \U0001f600\n')
