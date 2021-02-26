import pandas as pd

infile = open('Machine Learning\Jane Street Challenge\\train.csv')
out = open('Machine Learning\Jane Street Challenge\\test_set.csv','w')
line_count = 0
for line in infile:
    #if line_count < 1000:
    #    continue
    out.write(line)
    line_count += 1
    if line_count > 1000:
        break