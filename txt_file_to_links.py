import io

#
#
# Takes in string as name of file without '.txt' from which links will be read
# Returns list with a ", after each two lines
# Prints list of links
#
#
fileName = str(input('enter text file name: ')) + '.txt'
lineList = [line.rstrip('\n') for line in open(fileName)]
print(lineList)
