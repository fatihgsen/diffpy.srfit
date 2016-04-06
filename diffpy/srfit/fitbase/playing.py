#!/usr/bin/env python
from diffpy.Structure import loadStructure
from ase import Atoms
from ase.io import read
from ase.io import write
from ase.io import vasp
import numpy as np
from ase.calculators.vasp import Vasp

# Creates a VASP input from diffpy structure using ASE
        
 
def vaspcalc(struct):
    ats = Atoms(struct.element, scaled_positions=struct.xyz,cell=struct.lattice.stdbase)
    
    write('POSCAR',ats,format='vasp')
        
    ## run VASP here
    calc=Vasp(restart=None, 
    xc='PBE', 
    setups=None, 
    prec='Accurate', 
    algo='Fast', 
    ismear=0, 
    sigma=0.05,
    ediff=1E-5, 
    kpts=(10, 10, 10),
    isif=7,
    ibrion=2,
    isym=0, 
    gamma=None)
    
    calc.write_kpoints()
    calc.write_incar(self,ats)

    ats.set_calculator(calc)
    
    vaspout=read('OUTCAR',format='vasp_out')
    relaxed_struct=Atoms(struct.element, scaled_positions=vaspout.get_scaled_positions(),cell=vaspout.get_cell())
    energy=vaspout.get_potential_energy()
       
    return relaxed_struct, energy