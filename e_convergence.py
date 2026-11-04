import numpy as np
import matplotlib.pyplot as plt
import glob

def stitch_trajectories(file_paths):
    combined_time = []
    combined_e_total = []

    last_time = 0

    for i, path in enumerate(file_paths):
        data = np.loadtxt(path, skiprows=1)
        time, e_total = data[:, 0], data[:, 1]

        time_adjusted = time + last_time

        combined_time.extend(time_adjusted)
        combined_e_total.extend(e_total)

        last_time = time_adjusted[-1]

    return np.array(combined_time), np.array(combined_e_total)


file_paths = sorted(glob.glob('EComponents_*'))  

combined_time, combined_e_total = stitch_trajectories(file_paths)

plt.figure(figsize=(10, 6))
plt.plot(combined_time, combined_e_total, color='purple', linewidth=2)
plt.title('Stitched E(Total) vs. Time/fs')
plt.xlabel('Time (fs)')
plt.ylabel('E(Total)')
plt.grid(True)
plt.show()
