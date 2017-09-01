import csv
import sys

f = open(sys.argv[1], 'rt')
try:
    reader = csv.DictReader(f)
    for row in reader:
        print row
finally:
    f.close()
