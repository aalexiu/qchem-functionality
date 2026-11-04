import numpy as np
import re

def read_alpha_fock_matrix(filename, matrix_size=1670, values_per_line=6):
    start_reading = False
    matrix = np.zeros((matrix_size, matrix_size))  # initialize nxn matrix with zeros
    row_data_counts = [0] * matrix_size  # track how many values have been filled in each row
    float_pattern = re.compile(r"-?\d+\.\d{7}")  # find floats with exactly 7 decimal places
    time = -1

    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:  # EOF
                break

            if "Final Alpha Fock Matrix" in line:
                start_reading = True
                time += 1
                continue

            if "SCF time:" in line:
                if (time > 0):
                    np.save('fock/fock_' +str(time+0) + '.npy', matrix)
                start_reading = False
                matrix = np.zeros((matrix_size, matrix_size))  
                row_data_counts = [0] * matrix_size


            if start_reading:
                for row in range(matrix_size):
                    line = file.readline()
                    #print(line)
                    floats = float_pattern.findall(line)
                    if floats:
                        # convert strings to floats and add to the respective row in the matrix
                        start_col = row_data_counts[row]
                        end_col = start_col + len(floats)-1
                        matrix[row, start_col:end_col+1] = list(map(float, floats))
                        row_data_counts[row] += len(floats)

    return time


read_alpha_fock_matrix('aimd.out')
