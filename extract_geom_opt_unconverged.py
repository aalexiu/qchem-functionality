import numpy as np
import math

def get_geom(inputfile):
    flag=0
    with open(inputfile,'r') as inp:
    	for line in enumerate(inp):
            if ("   Optimization Cycle: 200\n" in line):
                flag = 1
                count = -3
            if ("   Point Group: c1    Number of degrees of freedom:   222\n" in line):
                flag=0
            if flag==1:
                count+=1
                if count>0:
                    line_split = line[1].split()
                    if (len(line_split)==5):
                        file = open("geometry.txt", "a")
                        file.write(line_split[1]+'   '+line_split[2]+'   '+line_split[3]+'   '+line_split[4]+'\n')
                        file.close()
    return

inputfile = 'cd38se38_opt.out'

get_geom(inputfile)