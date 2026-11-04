import numpy as np

np.set_printoptions(precision=10)

def get_num_orb(output):
    with open(output, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if "- Alpha" in line:
            n_orb=int(line.split()[3])
    return n_orb

def get_opdm(output):
    dm = np.zeros((n_orb, n_orb))

    with open(output, 'r') as file:
        lines = file.readlines()

    current_block = None
    buffer = []
    row_counter = 0

    for line in lines:
        line = line.strip()


        # Detect the start of a new block
        if "Printing g1p_bb_aa" in line:
            current_block = 'bb_aa'
            row_counter = 0
            buffer = []
            print(line)
        elif "g1p_bb_bb" in line:
            print(line)
            break
        elif current_block:
            # Skip non-numeric lines
            if any(char == 'e' for char in line):
                values = [float(x) for x in line.split()]
                buffer.extend(values)

                # Once we accumulate enough values per row, assign to 1RDM row and delete them from buffer
                if current_block == 'bb_aa' and len(buffer) >= n_orb:
                    dm[row_counter, 0:n_orb] = buffer[0:n_orb]
                    buffer = buffer[n_orb:]
                    row_counter += 1
    return dm

def get_opdm_separable(output):
    dm = np.zeros((n_orb, n_orb))

    with open(output, 'r') as file:
        lines = file.readlines()

    current_block = None
    buffer = []
    row_counter = 0

    for line in lines:
        line = line.strip()


        # Detect the start of a new block
        if "Printing g1s_bb_aa" in line:
            current_block = 'bb_aa'
            row_counter = 0
            buffer = []
            print(line)
        elif "g1s_bb_bb" in line:
            print(line)
            break
        elif current_block:
            # Skip non-numeric lines
            if any(char == 'e' for char in line):
                values = [float(x) for x in line.split()]
                buffer.extend(values)

                # Once we accumulate enough values per row, assign to 1RDM row and delete them from buffer
                if current_block == 'bb_aa' and len(buffer) >= n_orb:
                    dm[row_counter, 0:n_orb] = buffer[0:n_orb]
                    buffer = buffer[n_orb:]
                    row_counter += 1
    return dm

output='eom_ccsd.out'

n_orb = get_num_orb(output)
print("Number of orbitals:", n_orb)

with open('eom_ccsd.in.fchk_dens_correct', 'r') as rfileh:
    while True:  # loop over all lines
        try:
            line = next(rfileh)
            #print(line)
        except StopIteration:
            print("Reached end of file {}".format(rfileh.name))
            break

        if 'Overlap Matrix' in line:
            words = line.split()
            dim = int(words[-1])
            num_bas = int((2 * dim) ** 0.5)
            tmplist = []
            while len(tmplist) < dim:
                tmplist += next(rfileh).split()
            temp = np.zeros([num_bas, num_bas], float)
            temp[np.tril_indices(num_bas)] = tmplist
            S = np.triu(temp.T, 1) + temp
            print("Overlap matrix:")

dm_matrix = get_opdm(output) + get_opdm_separable(output)
print(dm_matrix)

print(np.diag(dm_matrix @ S))
print(np.trace(dm_matrix @ S))

eigenvalues,eigenvectors=np.linalg.eig(dm_matrix @ S)
print(eigenvalues)