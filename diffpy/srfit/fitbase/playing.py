#!/usr/bin/env python
from diffpy.Structure import loadStructure
from ase import Atoms
from ase.io import read
from ase.io import write
from ase.io import vasp
import numpy as np

# Creates a VASP input from diffpy structure using ASE

    def vaspcalc(struct,relaxed_struct,energy):
        ats = Atoms(struct.element, scaled_positions=struct.xyz,cell=struct.lattice.stdbase)
        write('POSCAR',ats,format='vasp')
        
        ## run VASP here
        
        vaspout=read('OUTCAR',format='vasp_out')
        relaxed_struct=Atoms(struct.element, scaled_positions=vaspout.get_scaled_positions(),cell=vaspout.get_cell())
        energy=vaspout.get_potential_energy()
        
        return