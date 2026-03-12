# Submit_Genome_Phase

## plot_dprof.py
Usage: python plot_dprof.py path/to/dprof0.073.txt
Used to plot the density of the slab along the z-scale (which is stored in a dprof_100.txt file) as a means of visually evaluating the results and to explain the methodology.


## high_low_rho.py
Looks for the dprof_100.txt files in the directories data25 and data30 corresponding to the different linker lengths. Note that I renamed the dprof_100.txt files to hve their specific salt concentration, exanple: dprof0.075.txt.
It then extracts the densities of the high density and low density phases and strores it in binodal_quantiles.csv.


## combined_phase_diagram.py
Plots the data from binodal_quantiles.csv and draws the phase diagram lines.
Some things to note:
frac=0.2: use lowest 20% bins for rho_low and highest 20% for rho_high, gives a good estimate based off of the poorly converged data.
ignore_zeros=True helps if you have empty padding regions, which there are a lot of in our data because it the simulation did not get to fully converge.

## density.py
################################################

I did not write density.py. This was written by Dr Maria Julia Maristany and all credit goes to her for the creation of density.py. It is include here because it is not in the other directores listed below.

This script creates the dprof_100.txt files, which contain the density profile data for a specifc slab simulation. It calculates it from the cores.dump file that the simulation creates.

################################################

## Other code used
All the other code, such as notably the lammps input files come from the following directory:
https://github.com/CollepardoLab/NucleosomeLinker
Some things to note:
Because the input files apply to the more general case, you commonly have to change the number of atom types in the data.txt files to 6, even though only 3 are present in the simultion to ensure that lammps does not crash because it sees a command for a particle that does not exist.
When bash create_simulation.sh was run, the salts given were 0.073, 0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.080, and each was given 120 fibers.
The exact input text files to create the lammps simulation input data as done when using this directory is given as linker_lengths_*.txt.


The version of lammps that was compiled and the correct modifications to add come from the following directory:
https://github.com/CollepardoLab/CollepardoLab_Chromatin_Model/tree/plugin-dev
Some things to note:
Make sure to use the plugin-dev version to give you the chromtin.so file, which you want to place in every directory in which you start a lammps simulation.


