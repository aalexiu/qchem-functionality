import numpy as np

def get_tot_energy():
    time = -1
    f_in = open('aimd.out', 'r')

    for line in f_in:
        if "Total energy in the final basis set" in line:
            time += 1
            if (time>0):
                energy = float(line.rsplit(" ",1)[1])
                f_out = open('energy.txt', "a")
                f_out.write(str(energy)+'\n')	
    return


get_tot_energy()
