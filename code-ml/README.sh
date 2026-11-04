Files needed to generate the AIMD trajectories, parse and save information for Ezra's Hamiltonian ML project.

- aimd.in and submit.sh: runs QChem AIMD. Prints out Fock matrix, MO coefficient matrix, energy at every time step
- get_tot_energy.py and energy.sh: parse AIMD output to get list of total SCF energy at each time step
- fock.py and run_fock_python.sh: parse AIMD output to get Fock matrix at every timestep. Returns fock_timestep.npy
- mo.py and run_mo_python.sh: parse AIMD output to get MO coeff matrix at every timestep. Returns mo_timestep.npy

Folder sad: files needed to print out all the same information for the geometries extracted at every time step of the trajectory, printing just the initial SAD guess instead of the converged SCF results.
- build_input.sh, qchem_out_to_in.py, change_filename.py: parses AIMD output file, and builds the input and submit files necessary to generate the SAD guess at each timestep in the trajectory.
- input_template.in, submit_template.sh: tempalte input and bash script to generate SAD guess (and not redo SCF cycle at each step)
- mass_submit.sh: submits all SAD runs generated using the scripts above
- job_done.sh: checks whether all SAD runs finished
- sad.py and run_sad_python.sh: parses all SAD outputs and get Fock matrix of SAD guess. Saves to sad_files/sad_timestep.npy
