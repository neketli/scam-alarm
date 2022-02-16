import csv
import sys
import argparse
import os
parser = str(sys.argv[1])

if parser.find( 'www.')>-1:
    n = parser.find('www.')+4
    parser = parser[n:]


if parser.find( '//')>-1:
    n = parser.find('//')+2
    parser = parser[n:]


if parser.find( '/')>-1:
    n = parser.find('/')
    parser = parser[:n]



delta = 1
results = []
results2 = []


with open(os.path.join("/home/lqbrqt/proj/hackathon-spring-2021-dstu/utils/pythonScripts/badwords.csv")) as csvfile:
    reader = csv.reader(csvfile, quotechar='\n')  # change contents to floats
    for row in reader:  # each row is a list
        results.append(row)

with open(os.path.join("/home/lqbrqt/proj/hackathon-spring-2021-dstu/utils/pythonScripts/domeins.csv")) as csvfile:
    reader = csv.reader(csvfile, quotechar='\n')  # change contents to floats
    for row in reader:  # each row is a list
        results2.append(row)



# test na вхождение "плохих слов"
for row in results:
    for index in row:
        if parser.find(index)>-1:
          delta = delta/1.5


# test na вхождение "плохих доменов"
parser_splitted = parser.split('.')
for row in results2:
    for index in row:
        for spl in parser_splitted:
            if index == spl:
              delta = delta/1.5

# kol -vo zifr
if delta !=0:
    zifri = len(list(filter(lambda m:m.isdigit(), str(parser))))
    if zifri - 2 > 0:
        delta = delta/(zifri-2)

# Проверка на подря идущие символы
count=1
i=0
j=1
while( i < len(parser)-1):
    while(j < len(parser)):
        while(parser[i]==parser[j]):
            j+=1
            count+=1
            if(j==len(parser)):
                if(count>2):
                    delta = delta/((count) * 0.75)

                    count=1
                break
        else:
            if(count>2):
                delta = delta/((count) * 0.75)

                count=1

                i=j
            j=j+1
    i=j
    j=j+1
    count=1

if(delta< 0.01):
    delta = 0.01
print(delta)