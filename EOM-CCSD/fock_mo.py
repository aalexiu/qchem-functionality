import numpy as np

def read_mo_coeff_matrix(filename, matrix_size=58):
    start_reading = False
    matrix_data = []

    with open(filename, 'r') as file:
        for line in file:
            if "Alpha MO coefficients" in line:
                start_reading = True
                continue

            if start_reading:
                matrix_data.extend(map(float, line.split()))

                if len(matrix_data) >= matrix_size ** 2:
                    break

    matrix = np.array(matrix_data[:matrix_size ** 2]).reshape((matrix_size, matrix_size))
    return matrix

import re


def read_alpha_fock_matrix(filename, matrix_size=58, values_per_line=6):
    start_reading = False
    matrix = np.zeros((matrix_size, matrix_size))  
    row_data_counts = [0] * matrix_size  
    float_pattern = re.compile(r"-?\d+\.\d{7}")  # Matches floats with exactly 7 decimal places

    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:  
                break

            if "Calculated Alpha Fock Matrix" in line:
                start_reading = True
                continue

            if "Extrapolated" in line:
                break

            if start_reading:
                for row in range(matrix_size):
                    line = file.readline()
                    floats = float_pattern.findall(line)
                    if floats:
                        start_col = row_data_counts[row]
                        end_col = start_col + len(floats)-1
                        #print(row, start_col, end_col, list(map(float, floats)))
                        matrix[row, start_col:end_col+1] = list(map(float, floats))
                        row_data_counts[row] += len(floats)

    return matrix


fock = read_alpha_fock_matrix('ccsd_full.out')

mo_coeff = read_mo_coeff_matrix('ccsd_full.in.fchk')

print(mo_coeff)