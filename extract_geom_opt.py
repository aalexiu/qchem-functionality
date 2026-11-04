import numpy as np
import math

def get_geom(inputfile):
    flag=0
    with open(inputfile,'r') as inp:
    	for line in enumerate(inp):
            if (" **  OPTIMIZATION CONVERGED  **\n" in line):
                flag = 1
                count = -5
            if ("Z-matrix Print:\n" in line):
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

inputfile = 'cd33se33_opt.out'

get_geom(inputfile)