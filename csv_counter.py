import csv
import urllib.request
#
#
# takes in string to name new file
# returns csv file with new name that has the data from the first gaia data light curve
# prints number of lines processed
#
url = 'http://cdn.gea.esac.esa.int/Gaia/gdr2/light_curves/csv/light_curves_1042504286338226688_1098703830327377408.csv.gz'
response = urllib.request.urlopen(url)
reader = csv.reader(response, 'r')
linNum=0
for line in reader:
    linNum=linNum + 1

print(linNum)
