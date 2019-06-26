import os
#
#
# Takes in name of the links text file as a string without ".txt"
# Prints out number of links in text file
#
#
fileName = str(input('enter text file name: ')) + '.txt'
lineList = [line.rstrip('\n') for line in open(fileName)]
dir = os.path.dirname(os.path.abspath(__file__))
num = len(lineList)

print(num)