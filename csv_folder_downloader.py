import csv
import urllib.request
import os
import gzip
import shutil
#
#
# Takes in string as name of new folder in which files will be stored.
# Unzips and returns csv files in folder with the name entered.
# Folder will be created in the directory of the location of the python code
# Files inside folder will be named 0 to x for the x files in gaia database
# 
#

newfolder = str(input('enter new folder name: '))
dir = os.path.dirname(os.path.abspath(__file__)) + '/' + newfolder
os.mkdir(dir)
url = ["http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1042504286338226688_1098703830327377408.csv.gz",
       "http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1098746200181562496_1150788044027782912.csv.gz",
       "http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1150901877842361600_1210969125779607680.csv.gz",
       "http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1211096291174493056_1265569498825687296.csv.gz",
       ]


for x in range(len(url)):
    newfile = dir + '/' + str(x) + '.csv'
    print(newfile)
    newfilegz = newfile + '.gz'

    urllib.request.urlretrieve(url[x], newfilegz)
    with gzip.open(newfilegz, 'rb') as f_in:
        with open(newfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(newfilegz)
