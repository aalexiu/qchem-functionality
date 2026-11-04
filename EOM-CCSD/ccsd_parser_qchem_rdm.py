import numpy as np

np.set_printoptions(precision=10, threshold = np.inf)

def swap_block(spin,n_max):
    if spin < n_max/2: # alpha block in bare QCHEM two-electron integrals
        return int(spin*2) # alpha becomes even index
    # beta block in bare QCHEM two-electron integrals
    return int(2*(spin-n_max/2)+1) # beta becomes odd index

def get_idx(Q, R, S, idx):
    p = idx // (Q*R*S)
    q = (idx - p*Q*R*S) // (R*S)
    r = (idx - p*Q*R*S - q*R*S) // S
    s = idx - p*Q*R*S - q*R*S - r*S
    return p, q, r, s

def parser(output):
    current_block = None
    buffer = []
    row_counter = 0
    with open(output, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line=line.strip()
            if "Active occupied" in line:
                n_occ = 2 * int(line.split()[3])
            elif "Active virtual" in line:
                n_virt = 2 * int(line.split()[3])

            elif "Printing T1" in line:
                current_block = 'T1'
                row_counter = 0
                buffer = []
                print(line)
                t1=np.zeros((n_occ,n_virt))
            elif "Printing T2" in line:
                current_block = 'T2'
                row_counter = 0
                buffer = []
                print(line)
                t2=np.zeros((n_occ,n_occ,n_virt,n_virt))
            elif "Printing L1" in line:
                current_block = 'L1'
                row_counter = 0
                buffer = []
                print(line)
                break
            elif current_block=='T1':
                # Skip non-numeric lines
                if any(char == 'e' for char in line):
                    values = [float(x) for x in line.split()]
                    buffer.extend(values)
                    # Once we accumulate enough values per row, assign to T1 row and delete them from buffer
                    if current_block == 'T1' and len(buffer) >= n_virt and row_counter < n_occ:
                        t1[row_counter, 0:n_virt] = buffer[0:n_virt]
                        buffer = buffer[n_virt:]
                        row_counter += 1

            elif current_block=='T2':
                # Skip non-numeric lines
                if any(char == 'e' for char in line):
                    values = [float(x) for x in line.split()]
                    buffer.extend(values)
                    # Once we accumulate enough values per row, assign to T1 row and delete them from buffer
                    if current_block == 'T1' and len(buffer) >= n_virt and row_counter < n_occ:
                        t1[row_counter, 0:n_virt] = buffer[0:n_virt]
                        buffer = buffer[n_virt:]
                        row_counter += 1


    return n_occ, n_virt#, t1, t2



def get_opdm(output):
    dm = np.zeros((n_occ+n_virt, n_occ+n_virt))
    rdm2_oooo = np.zeros((n_occ, n_occ, n_occ, n_occ))
    rdm2_ooov = np.zeros((n_occ, n_occ, n_occ, n_virt))
    rdm2_oovv = np.zeros((n_occ, n_occ, n_virt, n_virt))
    rdm2_ovoo = np.zeros((n_occ, n_virt, n_occ, n_occ))
    rdm2_ovov = np.zeros((n_occ, n_virt, n_occ, n_virt))
    rdm2_ovvv = np.zeros((n_occ, n_virt , n_virt , n_virt ))
    rdm2_vvoo = np.zeros((n_virt , n_virt , n_occ , n_occ ))
    rdm2_vvov = np.zeros((n_virt , n_virt , n_occ , n_virt ))
    rdm2_vvvv = np.zeros((n_virt , n_virt , n_virt , n_virt ))
    rdm2_oovo = np.zeros((n_occ , n_occ , n_virt , n_occ ))
    rdm2_vooo = np.zeros((n_virt , n_occ , n_occ , n_occ ))
    rdm2_voov = np.zeros((n_virt , n_occ , n_occ , n_virt ))
    rdm2_vovo = np.zeros((n_virt , n_occ , n_virt , n_occ ))
    rdm2_ovvo = np.zeros((n_occ , n_virt , n_virt , n_occ ))
    rdm2_vovv = np.zeros((n_virt , n_occ , n_virt , n_virt ))
    rdm2_vvvo = np.zeros((n_virt , n_virt , n_virt , n_occ ))


    with open(output, 'r') as file:
        lines = file.readlines()

    current_block = None
    buffer = []
    row_counter = 0

    for line in lines:
        line = line.strip()

        # Detect the start of a new block
        if "Printing CCSD DM_OO" in line:
            current_block = 'OO'
            row_counter = 0
            buffer = []
            print(line)
        elif "Printing CCSD DM_OV" in line:
            current_block = 'OV'
            row_counter = 0
            buffer = []
            print(line)
        elif "Printing CCSD DM_VO" in line:
            current_block = 'VO'
            row_counter = n_occ
            buffer = []
            print(line)
        elif "Printing CCSD DM_VV" in line:
            current_block = 'VV'
            row_counter = n_occ
            buffer = []
            print(line)

        elif "CCSD 2RDM_OOOO" in line:
            current_block = 'OOOO'
            buffer=[]
        elif "CCSD 2RDM_OOOV" in line:
            current_block = 'OOOV'
            buffer=[]
        elif "CCSD 2RDM_OOVV" in line:
            current_block = 'OOVV'
            buffer=[]
        elif "CCSD 2RDM_OVOO" in line:
            current_block = 'OVOO'
            buffer=[]
        elif "CCSD 2RDM_OVOV" in line:
            current_block = 'OVOV'
            buffer=[]
        elif "CCSD 2RDM_OVVV" in line:
            current_block = 'OVVV'
            buffer=[]
        elif "CCSD 2RDM_VVOO" in line:
            current_block = 'VVOO'
            buffer=[]
        elif "CCSD 2RDM_VVOV" in line:
            current_block = 'VVOV'
            buffer=[]
        elif "CCSD 2RDM_VVVV" in line:
            current_block = 'VVVV'
            buffer=[]

        #elif "Reference state properties" in line:
        elif "CCSD calculation:" in line:
            rdm2 = np.block([[[[rdm2_oooo, rdm2_ooov], [rdm2_oovo, rdm2_oovv]],
                             [[rdm2_ovoo, rdm2_ovov],[rdm2_ovvo, rdm2_ovvv]]],
                             [[[rdm2_vooo, rdm2_voov], [rdm2_vovo, rdm2_vovv]],
                             [[rdm2_vvoo, rdm2_vvov],[rdm2_vvvo, rdm2_vvvv]]]])
            print(np.shape(rdm2))

            break

        elif current_block:
            # Skip non-numeric lines
            if any(char == 'e' for char in line) and ('S^2' not in line):
                values = [float(x) for x in line.split()]
                buffer.extend(values)

                # Once we accumulate enough values per row, assign to 1RDM row and delete them from buffer
                if current_block == 'OO' and len(buffer) >= n_occ:
                    dm[row_counter, 0:n_occ] = buffer[0:n_occ]  # Fill top-left block
                    buffer = buffer[n_occ:]
                    row_counter += 1
                elif current_block == 'OV' and len(buffer) >= n_virt:
                    dm[row_counter, n_occ:] = buffer[0:n_virt]  # Fill top-right block
                    buffer = buffer[n_virt:]
                    row_counter += 1
                elif current_block == 'VO' and len(buffer) >= n_occ:
                    dm[row_counter, 0:n_occ] = buffer[0:n_occ]  # Fill bottom-left block
                    buffer = buffer[n_occ:]
                    row_counter += 1
                elif current_block == 'VV' and len(buffer) >= n_virt:
                    dm[row_counter, n_occ:] = buffer[0:n_virt]  # Fill bottom-right block
                    buffer = buffer[n_virt:]
                    row_counter += 1
                    if (row_counter >= n_occ+n_virt):
                        current_block = None

                elif current_block == 'OOOO' and len(buffer) == n_occ ** 4:
                    print('OOOO')
                    P = n_occ
                    Q = n_occ
                    R = n_occ
                    S = n_occ
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_oooo [p,q,r,s] = buffer[idx]
                        '''if (p < P  and q < Q  and r < R  and s < S ):
                            rdm2_oooo [p,q,r,s] = 2* buffer[idx]''' ### multiply by 2 for spin-traced
                
                elif current_block == 'OOOV' and len(buffer) == n_occ ** 3 * n_virt:
                    P = n_occ
                    Q = n_occ
                    R = n_occ
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_ooov [p,q,r,s] = buffer[idx]
                    
                    ### OOOV = -OOVO

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_oovo[p,q,s,r] = - rdm2_ooov[p,q,r,s]

                elif current_block == 'OOVV' and len(buffer) == n_occ ** 2 * n_virt ** 2:
                    P = n_occ
                    Q = n_occ
                    R = n_virt
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_oovv [p,q,r,s] = buffer[idx]


                elif current_block == 'OVOO' and len(buffer) == n_occ ** 3 * n_virt:
                    P = n_occ
                    Q = n_virt
                    R = n_occ
                    S = n_occ
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_ovoo [p,q,r,s] = buffer[idx]
                    
                    ### OVOO = -VOOO

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_vooo[q,p,r,s] = - rdm2_ovoo[p,q,r,s]

                elif current_block == 'OVOV' and len(buffer) == n_occ ** 2 * n_virt ** 2:
                    P = n_occ
                    Q = n_virt
                    R = n_occ
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_ovov [p,q,r,s] = buffer[idx]
                    
                    ### OVOV = -VOOV

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_voov[q,p,r,s] = - rdm2_ovov[p,q,r,s]

                    ### OVOV = VOVO

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_vovo[q,p,s,r] = rdm2_ovov[p,q,r,s]

                    ### OVOV = -OVVO

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_ovvo[p,q,s,r] = - rdm2_ovov[p,q,r,s]

                elif current_block == 'OVVV' and len(buffer) == n_occ * n_virt ** 3:
                    P = n_occ
                    Q = n_virt
                    R = n_virt
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_ovvv [p,q,r,s] = buffer[idx]
                    
                    ### OVVV = -VOVV

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_vovv[q,p,r,s] = - rdm2_ovvv[p,q,r,s]

                elif current_block == 'VVOO' and len(buffer) == n_occ ** 2 * n_virt ** 2:
                    P = n_virt
                    Q = n_virt
                    R = n_occ
                    S = n_occ
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_vvoo [p,q,r,s] = buffer[idx]
                            

                elif current_block == 'VVOV' and len(buffer) == n_occ * n_virt ** 3:
                    P = n_virt
                    Q = n_virt
                    R = n_occ
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_vvov [p,q,r,s] = buffer[idx]
                    
                    ### VVOV = -VVVO

                    for p in range (P ):
                        for q in range (Q ):
                            for r in range (R ):
                                for s in range (S ):
                                    rdm2_vvvo[p,q,s,r] = - rdm2_vvov[p,q,r,s]
                
                elif current_block == 'VVVV' and len(buffer) == n_virt ** 4:
                    P = n_virt
                    Q = n_virt
                    R = n_virt
                    S = n_virt
                    for idx in range(len(buffer)):
                        p, q, r, s = get_idx(Q, R, S, idx)
                        rdm2_vvvv [p,q,r,s] = buffer[idx] 

    return dm, rdm2


def spin_traced (dm_matrix):
    #dm = np.zeros(((n_occ+n_virt)/2, (n_occ+n_virt)/2))

    dm_upper = np.hstack((dm_matrix[0:(n_occ//2 ), 0:(n_occ//2 )], dm_matrix[0:(n_occ//2 ), n_occ:(n_occ+n_virt//2 )]))
    print(np.shape(dm_upper))

    dm_lower = np.hstack((dm_matrix[n_occ:n_occ+n_virt//2 , 0:n_occ//2 ], dm_matrix[n_occ:n_occ+n_virt//2 , n_occ:n_occ+n_virt//2 ]))
    print(np.shape(dm_lower))

    dm = np.vstack((dm_upper, dm_lower))
    return dm


output='eom.out'

#n_occ, n_virt, t1, t2 = parser(output)

n_occ, n_virt = parser(output)
print("Number of active occupied orbitals:", n_occ)
print("Number of active virtual orbitals:", n_virt)


dm_matrix, rdm2 = get_opdm(output)
print("1RDM spin-orbital basis")
print(dm_matrix) ###spin-separated alpha alpha...beta beta... order

#swap to pyscf orbital ordering
dm1_pyscf_order = np.zeros((n_occ+n_virt, n_occ+n_virt))
###OO block
for i in range (n_occ):
    for j in range(n_occ):
        # swap spin block; [aa..abbb..b] -> [abab..ab]
        p,q = swap_block(i,n_occ),swap_block(j,n_occ)
        print(i,j)
        print(p,q)
        print(dm_matrix[i,j])
        dm1_pyscf_order[p,q]=dm_matrix[i,j]

print("OV")
###OV block
for i in range(n_occ):
    for j in range(n_occ, n_occ+n_virt):
        # swap spin block; [aa..abbb..b] -> [abab..ab]
        p,q = swap_block(i,n_occ),swap_block(j-n_occ,n_virt)
        print(i,j)
        print(p,q+n_occ)
        print(dm_matrix[i,j])
        dm1_pyscf_order[p,q+n_occ]=dm_matrix[i,j]

###VO block
for i in range(n_occ,n_occ+n_virt):
    for j in range(n_occ):
        # swap spin block; [aa..abbb..b] -> [abab..ab]
        p,q = swap_block(i-n_occ,n_virt),swap_block(j,n_occ)
        dm1_pyscf_order[p+n_occ,q]=dm_matrix[i,j]

###VV block
for i in range(n_occ, n_occ+n_virt):
    for j in range(n_occ, n_occ+n_virt):
        # swap spin block; [aa..abbb..b] -> [abab..ab]
        p,q = swap_block(i-n_occ,n_virt),swap_block(j-n_occ,n_virt)
        dm1_pyscf_order[p+n_occ,q+n_occ]=dm_matrix[i,j]


print("reorder 1rdm")
print(dm1_pyscf_order)

### multiply by two (both alpha and beta spins)
dm_spin_tr = 2 * spin_traced(dm_matrix)
print(dm_spin_tr)

### add HF part (separable) to 1RDM
for i in range(n_occ//2 ):
    dm_spin_tr[i,i] += 2

### add separable part to 2RDM

'''gamma_ref=np.zeros(((n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ))
#corrects for double-counting of the reference determinant contributions

for i in range((n_occ+n_virt) ):
    for j in range((n_occ+n_virt) ):
        for k in range((n_occ+n_virt) ):
            for l in range((n_occ+n_virt) ):
                if (l==i and k==j):
                    gamma_ref[i,j,k,l] -= 1
                if (k==i and l==j):
                    gamma_ref[i,j,k,l] += 1

delta = np.zeros(((n_occ+n_virt) , (n_occ+n_virt) ))
for i in range (n_occ ):
    delta[i,i] = 1

rdm2_sep = np.zeros(((n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ))


#opdm = spin_traced(dm_matrix)
opdm = dm_spin_tr/2


for p in range((n_occ+n_virt) ):
    for q in range((n_occ+n_virt) ):
        for r in range((n_occ+n_virt) ):
            for s in range((n_occ+n_virt) ):
                rdm2_sep[p,q,r,s] = delta[r,p] * opdm[q,s] - delta[r,q] * opdm[p,s] + delta[s,q] * opdm[p,r] - delta[s,p] * opdm[q,r]
                rdm2_sep[p,q,r,s] -= gamma_ref[p,q,r,s]'''

gamma_ref=np.zeros(((n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt)))
#corrects for double-counting of the reference determinant contributions

for i in range((n_occ)):
    for j in range((n_occ)):
        for k in range((n_occ)):
            for l in range((n_occ)):
                if (l==i and k==j):
                    gamma_ref[i,j,k,l] -= 1
                if (k==i and l==j):
                    gamma_ref[i,j,k,l] += 1

delta = np.zeros(((n_occ+n_virt), (n_occ+n_virt)))
for i in range (n_occ):
    delta[i,i] = 1

rdm2_sep = np.zeros(((n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt)))


#opdm = spin_traced(dm_matrix)
opdm = dm1_pyscf_order+delta


for p in range((n_occ+n_virt)):
    for q in range((n_occ+n_virt)):
        for r in range((n_occ+n_virt)):
            for s in range((n_occ+n_virt)):
                rdm2_sep[p,q,r,s] = delta[r,p] * opdm[q,s] - delta[r,q] * opdm[p,s] + delta[s,q] * opdm[p,r] - delta[s,p] * opdm[q,r]
                rdm2_sep[p,q,r,s] -= gamma_ref[p,q,r,s]

#rdm2_2 = np.zeros(((n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ,(n_occ+n_virt) ))


'''for i in range((n_occ+n_virt) ):
    for j in range((n_occ+n_virt) ):
        for k in range((n_occ+n_virt) ):
            for l in range((n_occ+n_virt) ):
                if (i==k and j==l):
                    rdm2_2[i,j,k,l] += 4
                if (i==l and k==j):
                    rdm2_2[i,j,k,l] -=2'''


'''print("1RDM:")
print(dm_spin_tr)'''


print("1RDM)")
print(dm_matrix+delta)

print("2RDM sep")
#print(rdm2[0,1] + 2*rdm2_sep[0,1])
#print(rdm2_sep)
print("2RDM")
#print(rdm2)
print("2RDM total")
rdm2_tot=rdm2#+rdm2_sep #remove rdm2_sep to hopefully match quemb code....

###Reorder 2RDM from alpha alpha...beta beta to alpha beta alpha beta...

rdm2_pyscf_order = np.zeros(((n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt),(n_occ+n_virt)))


def reorder_2rdm(imin,jmin,kmin,lmin,imax,jmax,kmax,lmax):
    for i in range(imin, imax):
        for j in range(jmin, jmax):
            for k in range (kmin, kmax):
                for l in range (lmin,lmax):
                    # swap spin block; [aa..abbb..b] -> [abab..ab]
                    p,q,r,s = swap_block(i-imin,imax-imin),swap_block(j-jmin,jmax-jmin), swap_block(k-kmin,kmax-kmin), swap_block(l-lmin,lmax-lmin)
                    rdm2_pyscf_order[p+imin,q+jmin,r+kmin,s+lmin]=rdm2_tot[i,j,k,l]
    return

###do for each block separately and then reconstruct full 2rdm
#then integrate over spin at the next step
###1rdm still not correct (some elements are - what they should be?)


'''or i in range(n_occ,n_occ+n_virt):
    for j in range(n_occ):
        # swap spin block; [aa..abbb..b] -> [abab..ab]
        p,q = swap_block(i-n_occ,n_virt),swap_block(j,n_occ)
        dm1_pyscf_order[p+n_occ,q]=dm_matrix[i,j]'''

###OOOO block
reorder_2rdm(0,0,0,0,n_occ,n_occ,n_occ,n_occ)
#OOOV
reorder_2rdm(0,0,0,n_occ,n_occ,n_occ,n_occ,n_occ+n_virt)
#OOVO
reorder_2rdm(0,0,n_occ,0,n_occ,n_occ,n_occ+n_virt,n_occ)
#OOVV
reorder_2rdm(0,0,n_occ,n_occ,n_occ,n_occ,n_occ+n_virt,n_occ+n_virt)

#OVOO
reorder_2rdm(0,n_occ,0,0,n_occ,n_occ+n_virt,n_occ,n_occ)
#OVOV
reorder_2rdm(0,n_occ,0,n_occ,n_occ,n_occ+n_virt,n_occ,n_occ+n_virt)
#OVVO
reorder_2rdm(0,n_occ,n_occ,0,n_occ,n_occ+n_virt,n_occ+n_virt,n_occ)
#OVVV
reorder_2rdm(0,n_occ,n_occ,n_occ,n_occ,n_occ+n_virt,n_occ+n_virt,n_occ+n_virt)

#VOOO
reorder_2rdm(n_occ,0,0,0,n_occ+n_virt,n_occ,n_occ,n_occ)
#VOOV
reorder_2rdm(n_occ,0,0,n_occ,n_occ+n_virt,n_occ,n_occ,n_occ+n_virt)
#VOVO
reorder_2rdm(n_occ,0,n_occ,0,n_occ+n_virt,n_occ,n_occ+n_virt,n_occ)
#VOVV
reorder_2rdm(n_occ,0,n_occ,n_occ,n_occ+n_virt,n_occ,n_occ+n_virt,n_occ+n_virt)

#VVOO
reorder_2rdm(n_occ,n_occ,0,0,n_occ+n_virt,n_occ+n_virt,n_occ,n_occ)
#VVOV
reorder_2rdm(n_occ,n_occ,0,n_occ,n_occ+n_virt,n_occ+n_virt,n_occ,n_occ+n_virt)
#VVVO
reorder_2rdm(n_occ,n_occ,n_occ,0,n_occ+n_virt,n_occ+n_virt,n_occ+n_virt,n_occ)
#VVVV
reorder_2rdm(n_occ,n_occ,n_occ,n_occ,n_occ+n_virt,n_occ+n_virt,n_occ+n_virt,n_occ+n_virt)


print("REORDERED 2rdm")
#print(rdm2_pyscf_order)

n_mo=(n_occ+n_virt)//2

rdm2_spin_tr=np.zeros((n_mo,n_mo,n_mo,n_mo))


for p in range(2*n_mo):
    for q in range(2*n_mo):
        for r in range(2*n_mo):
            for s in range(2*n_mo):
                if (r%2==p%2 and s%2==q%2):
                    rdm2_spin_tr[p//2,r//2,q//2,s//2] += rdm2_pyscf_order[p,q,r,s] #rdm2_tot[p,q,r,s]

print("spin traced 2RDM")
#print(rdm2_spin_tr)

print(dm_spin_tr)

with open('ccsd-frag0-1rdm.npy', 'wb') as f:
    np.save(f,dm_spin_tr)

with open('ccsd-frag0-2rdm.npy', 'wb') as f:
    np.save(f,rdm2_spin_tr)

###both 1 and 2 RDMS are in the MO basis, and are spin-traced (also have the factor of 2)
###both also have the HF part added d_ijkl = D_ij*D_kl - 0.5*D_il*D_kj
#unrelaxed
