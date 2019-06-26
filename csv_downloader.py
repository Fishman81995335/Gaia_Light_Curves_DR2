import csv
import urllib.request
import os
import gzip
import shutil
#
#
# takes in string as name of new file
# unzips and returns csv file with new name that has the data from the gaia 
# data light curve file in same directory as python file
#

newfile = str(input('enter new file name: '))
dir = os.path.dirname(os.path.abspath(__file__))
newfilegz = dir + '/' + newfile + '.csv.gz'
newfile = dir + '/' + newfile + '.csv'
url = "http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1042504286338226688_1098703830327377408.csv.gz"
urllib.request.urlretrieve(url, newfilegz)

with gzip.open(newfilegz, 'rb') as f_in:
    with open(newfile, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
os.remove(newfilegz)
