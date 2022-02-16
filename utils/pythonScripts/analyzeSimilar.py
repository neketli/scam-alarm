import csv
import sys

domain = str(sys.argv[1])
#domain = input()
if domain.find( 'www.')>-1:
    n = domain.find('www.')+4
    domain = domain[n:]


if domain.find( '//')>-1:
    n = domain.find('//')+2
    domain = domain[n:]


if domain.find( '/')>-1:
    n = domain.find('/')
    domain = domain[:n]

results = []
with open("/home/lqbrqt/proj/hackathon-spring-2021-dstu/utils/pythonScripts/top500.csv") as csvfile:
    reader = csv.reader(csvfile, quotechar='\n')  # change contents to floats
    for row in reader:  # each row is a list
        results.append(row)


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


scores = dict()

maxVal = -1000

ratio = 1


for r in results:
    value = 1 - levenshteinDistance(domain, r[0])
    if(value > maxVal):
        maxVal = value

    if domain.rsplit( ".", 1 )[ 0 ].find(r[0].rsplit( ".", 1)[ 0 ]) != -1 and domain.rsplit( ".", 1 )[ 0 ] != r[0].rsplit( ".", 1)[ 0 ] and len(r[0].rsplit( ".", 1)[ 0 ]) > 3:
            ratio = 0.1


if  -5 < maxVal < 1:
    ratio = 0.1
if(ratio< 0.01):
    ratio = 0.01
print(ratio)
