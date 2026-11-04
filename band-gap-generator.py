import re

HARTREE_TO_EV = 27.2114

def extract_gaps(filename="cd33.out", output="gap.txt"):
    gaps_ev = []
    
    with open(filename, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "-- Virtual --" in line:
            
            j = i - 1
            while j >= 0 and not re.search(r"[-+]?\d*\.\d+", lines[j]):
                j -= 1
            
            if j < 0:
                continue
            
            occ_line = lines[j]
            
            k = i + 1
            while k < len(lines) and not re.search(r"[-+]?\d*\.\d+", lines[k]):
                k += 1
            
            if k >= len(lines):
                continue
            
            virt_line = lines[k]
            
            occ_energies = [float(x) for x in occ_line.split()]
            virt_energies = [float(x) for x in virt_line.split()]
            
            if not occ_energies or not virt_energies:
                continue
            
            homo = occ_energies[-1]
            
            lumo = virt_energies[0]
            
            gap_hartree = lumo - homo
            gap_ev = gap_hartree * HARTREE_TO_EV
            
            gaps_ev.append(gap_ev)

    with open(output, "w") as f:
        for gap in gaps_ev:
            f.write(f"{gap:.6f}\n")

extract_gaps("5/aimd_5.out", "gap.txt")
