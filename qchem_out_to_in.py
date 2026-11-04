
import sys

def grep(index, file): 
  ### read output file content
    f_data = open(file, 'r')

    count = 0
    start = False
    for line in f_data:
        count += 1
        if count==(index)*62+3: 
            start = True
            f_out = open("sad.in","w+")
            f_out.write("$molecule\n0 1\n")
        
        if start==True:
            f_out.write(line)
        
        # Stop Writing and close file
        if count==(index+1)*62:
            start = False
            f_out.write("$end\n\n$rem\nmethod pbe\nbasis sto-3g\necp fit-lanl2dz\n"+\
                "mem_total 5000\nmem_static 1000\nithrsh_dft 15\nsym_ignore = true\nscf_guess sad\nmax_scf_cycles 0\nscf_print 2\nxc_grid 000075000302\n$end")
            f_out.close()
            break
    f_data.close()

### Time steps to output
try:
    if sys.argv.__len__() > 1:
        index = int(sys.argv[1])
except:
    print("index not added")

#grep('TIME STEP', 'test.txt')
grep(index, "View.xyz")
