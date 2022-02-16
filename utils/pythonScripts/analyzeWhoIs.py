import whois
import sys
from datetime import datetime
from datetime import timedelta
now = datetime.now()


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
try:

    domain = whois.query(parser)


    ratio = 1

    deltatime = now - domain.creation_date


    if deltatime < timedelta(days = 6*30):
        ratio = ratio * 0
    elif (deltatime)< timedelta(days = 365):
        ratio = ratio * (deltatime)/timedelta(days = 365)
except Exception:
    ratio = 0.1

if(ratio< 0.01):
    ratio = 0.01
print(ratio)

