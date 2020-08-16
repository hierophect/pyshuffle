import csv
import sys

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(f"{{\"e\":\"{row[0]}\",\"h\":\"{row[2]}\",\"k\":\"{row[1]}\"}},")