import matplotlib.pyplot as plt
import numpy as np
import os

system = input("What is your chemical system? This name will go on your plots: ")

#Bandgap calculation/plotting:
# Constants for the particle in a sphere calculation
Egap = 1.74*1.6021766339999E-19 #Jc
h = 6.62607015e-34  # J*s (Planck's constant)
me = 9.10938356e-31  # kg (electron mass in kg)
melec = 0.13 * me
mh = 0.45 * me

# Dictionary to map elements to their atomic masses (in amu, which is fine as they cancel out in the calculations)
atomic_masses = {
    'Cd': 112.41,
    'Se': 78.971
}

def parse_coordinates(file_content):
    coordinates_list = []
    masses_list = []
    in_block = False
    block = []
    mass_block = []

    for line in file_content:
        if "Standard Nuclear Orientation (Angstroms)" in line:
            in_block = True
            skip_lines = 2  # Skip the next two lines
            continue

        if in_block:
            if skip_lines > 0:
                skip_lines -= 1
                continue

            if "-----" in line:
                if block:
                    coordinates_list.append(np.array(block))
                    masses_list.append(np.array(mass_block))
                block = []
                mass_block = []
                in_block = False
                continue

            parts = line.split()
            if len(parts) >= 5:
                element = parts[1]
                x = float(parts[2]) * 1e-10  # Convert Å to meters
                y = float(parts[3]) * 1e-10
                z = float(parts[4]) * 1e-10
                block.append([x, y, z])
                mass_block.append(atomic_masses.get(element, 0))  # Get mass, default to 0 if element not found

    return coordinates_list, masses_list

def calculate_bandgap_energy(coordinates, masses):
    total_mass = np.sum(masses)
    if total_mass == 0:
        return 0.0

    # Compute center of mass
    com = np.sum(coordinates.T * masses, axis=1) / total_mass

    # Calculate squared distances from center of mass
    squared_distances = np.sum((coordinates - com) ** 2, axis=1)

    # Calculate radius of gyration
    radius_of_gyration = np.sqrt(np.mean(squared_distances))
    print(radius_of_gyration*np.sqrt(5/3))
    # Calculate bandgap energy
    bandgap_energy = (Egap + (h**2) * (1/melec + 1/mh) / (8 * (5/3) * radius_of_gyration**2))*6.241509074461e18
    #print(bandgap_energy)
    return bandgap_energy

def main(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    coordinates_list, masses_list = parse_coordinates(file_content)

    bandgap_energies = []
    for i, (coordinates, masses) in enumerate(zip(coordinates_list, masses_list)):
        Ebandgap = calculate_bandgap_energy(coordinates, masses)
        bandgap_energies.append(Ebandgap)

    return bandgap_energies

# Generate x-axis values with increment
x_values = [0.99174 * i for i in range(200)]

# Replace 'aimd.out' with the path to your input file
file_path = 'aimd_12.out'
bandgap_energies = main(file_path)
plt.figure(figsize=(20, 14))
plt.plot(range(1, len(bandgap_energies) + 1), bandgap_energies, marker='o', linestyle='', color='g')
plt.ylabel('Bandgap Energy (eV)', fontsize=44)
plt.xlabel('Time (fs)', fontsize=44)
plt.xlim(min(x_values),max(x_values))
plt.title('Bandgap During Trajectory of '+ system, fontsize=60)
plt.tick_params(axis='y', which='major', labelsize=44)
plt.tight_layout()
plt.savefig("bandgap.jpg")
