import numpy as np
import re

def read_alpha_fock_matrix(filename, matrix_size=300, values_per_line=6):
    start_reading = False
    matrix = np.zeros((matrix_size, matrix_size)) 
    row_data_counts = [0] * matrix_size 
    float_pattern = re.compile(r"-?\d+\.\d{7}") 

    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:  # EOF
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


fock = read_alpha_fock_matrix('sad.out')
np.save('sad.npy', fock)
