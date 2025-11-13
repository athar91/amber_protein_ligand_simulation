# Molecular Dynamics Simulation Tutorial

This tutorial guides you for setting up and running a molecular dynamics (MD) simulation for a protein-ligand complex using the AMBER molecular dynamics software suite. This tutorial is a part of course of "Molecular Modeling of biological System" of Department of Physics, University of Cagliari.

<img width="460" height="583" alt="amber" src="https://github.com/user-attachments/assets/71a15ed8-52ed-480b-9661-e9418cc11edb" />

## Introduction
In this tutorial, we will simulate the prescription drug Sustiva (Efavirenz) in complex with HIV-1 REVERSE TRANSCRIPTASE. Efavirenz is a human immunodeficiency virus type 1 (HIV-1) specific, non-nucleoside, reverse transcriptase (RT) inhibitor marketed by Bristol Myers Squibb for controlling the progression of HIV infection in humans.
The chemical name for Sustiva is  (S)-6-chloro-(cyclopropylethynyl)-1,4-dihydro-4-(trifluoromethyl)-2H-3,1-benzoxazin-2-one.
The Efavirenz bound RT pdb file is downloaded from (PDB ID [1FKO](https://www.rcsb.org/structure/1FKO)). The coordinates of sustiva are associated with a residue called "EFZ" (Efavirenz).

<img width="742" height="308" alt="drug" src="https://github.com/user-attachments/assets/d0022fbc-92a1-4ae5-8943-60b59b828918" />

The files are also available at altair server of physics department (dsf.unica.it): @altair:/scratch/mathar/Tutorial8_amber_protein_ligand_simulation-main.zip

## Test Environment
The tutorial assumes the following test environment:

```bash
mathar@freddie:~/cheetah/andrea_files/try/tutorial8 

### Source the amber program


```
## Steps

## 1. Download PDB Structure
Download a PDB structure file for your protein-ligand complex. In this tutorial, we'll use the example structure `1fko.pdb`.


## 2. Prepare Protein Structure
Open the PDB structure in VMD and save only the protein coordinates using the following VMD selection:
```bash
(chain A and resid 1 to 243 or resname EFZ)
```
Save the protein structure as 1fko_trunc.pdb.

## 3. Clean and Prepare Ligand
Clean the ligand structure using pdb4amber, grep, reduce, and antechamber. Run the following commands:

pdb4amber is a tool that helps to preprocess PDB files for AMBER simulations.
```bash
pdb4amber -i 1fko_trunc.pdb -o 1fko_trunc_clean.pdb --add-missing-atoms --no-reduce-db --most-populous
```


grep EFZ
```bash
grep EFZ 1fko_trunc_clean.pdb > EFZ.pdb
grep -v EFZ 1fko_trunc_clean.pdb > prot.pdb
```
We will investigate the protonation states of the protein using the H++ web server (available at http://newbiophysics.cs.vt.edu/H++/).
This server estimates pKₐ values of ionizable residues and assigns appropriate protonation states at a specified pH using continuum electrostatics.
To use it, register on the server, upload the protein structure file (prot.pdb), and process it to generate a protonated model.
The resulting structure, with optimized hydrogen placement and assigned charge states, can then be used for further molecular dynamics simulations.

reduce is a tool for adding hydrogen atoms to a PDB file
```bash
reduce EFZ.pdb > EFZ_H.pdb
```
 antechamber: We shall use Antechamber to assign atom types to this molecule and also calculate a set of point charges. Antechamber is the most important program within the set of Antechamber tools. It can perform many file conversions and can also assign atomic charges and atom types. Depending on its inputs, antechamber executes the following programs (all provided with AmberTools): sqm, atomtype, am1bcc, bondtype, espgen, respgen and prepgen.
```bash
antechamber -i EFZ_H.pdb -fi pdb -o EFZ_H.mol2 -fo mol2 -c bcc -s 2
```
Alternatively, you can use Acpype server to generate the forcefield topology using https://www.bio2byte.be/acpype/

parmchk2 to test if all the parameters we require are available
```bash
parmchk2 -i EFZ_H.mol2 -f mol2 -o EFZ_H.frcmod
```
# 4. Create Leap Input Files
tleap is a program that will generate the system from the command line based on an input file containing all the necessary information Create two TLEAP input files (tleap.in and tleap2.in) with the provided content.

[tleap.in](tleap.in)
```bash
source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.tip3p
EFZ = loadmol2 EFZ_H.mol2
check EFZ
loadamberparams EFZ_H.frcmod
saveoff EFZ ligand.lib
saveamberparm EFZ ligand.prmtop ligand.inpcrd
quit
```
Open ligand.prmtop and try to understand the parameters.
%FLAG TITLE: Describes the system or molecule name (e.g., EFZ).

%FLAG POINTERS: Contains numerical counts — total number of atoms, bonds, angles, dihedrals, atom types, residues, etc.
These values tell Amber how to interpret the rest of the data.

%FLAG ATOM_NAME: Lists the names of all atoms in the system (e.g., C1, O1, N1, H1…).

%FLAG CHARGE: Contains the partial atomic charges (scaled by 18.2223).
Divide each value by 18.2223 to get the charge in e (elementary charge units).

%FLAG ATOMIC_NUMBER: Gives the atomic number of each atom (e.g., 6 for carbon, 8 for oxygen, 1 for hydrogen).

%FLAG MASS: Lists the atomic masses used for each atom (in atomic mass units).

%FLAG BONDS_WITHOUT_HYDROGEN: Defines all covalent bonds not involving hydrogen atoms.Each bond entry contains atom indices and a bond type, which links to the bond parameters.
%FLAG BONDS_INC_HYDROGEN: Defines all bonds that include hydrogen atoms.
%FLAG BOND_FORCE_CONSTANT: Stores the bond stretching force constants (k) in kcal/mol·Å².
%FLAG BOND_EQUIL_VALUE: Contains the equilibrium bond lengths (r₀) in Ångström.
%FLAG ANGLES_WITHOUT_HYDROGEN: Lists all angles between three bonded atoms that do not include hydrogen.
%FLAG ANGLES_INC_HYDROGEN: Lists all angles that include hydrogen atoms.
%FLAG ANGLE_FORCE_CONSTANT: Angle bending force constants (kθ) in kcal/mol·rad².
%FLAG ANGLE_EQUIL_VALUE: Equilibrium bond angles (θ₀) in degrees.
%FLAG DIHEDRALS_WITHOUT_HYDROGEN: Defines torsional angles (four connected atoms) without hydrogen.
%FLAG DIHEDRALS_INC_HYDROGEN: Defines torsional angles that include hydrogen atoms.
%FLAG DIHEDRAL_FORCE_CONSTANT: Contains torsional barrier heights (Vn/2) in kcal/mol.
%FLAG DIHEDRAL_PERIODICITY: Lists periodicity (n) for each dihedral — the number of minima per 360° rotation.
%FLAG DIHEDRAL_PHASE: Contains phase offsets (γ) in degrees for each torsion.
%FLAG NONBONDED_PARM_INDEX: Defines which pair of atom types use which nonbonded parameter set.
%FLAG LENNARD_JONES_ACOEF: Lennard–Jones A coefficients used in the 12-6 potential term 
%FLAG LENNARD_JONES_BCOEF: Lennard–Jones B coefficients used in the 12-6 potential term 
%FLAG RESIDUE_LABEL: Lists residue names (e.g., LIG, ALA, H2O).
%FLAG RESIDUE_POINTER: Indicates the starting atom index for each residue.
%FLAG BOX_DIMENSIONS: (Only present for solvated systems) — gives the box lengths (a, b, c) and angles (α, β, γ) for periodic boundary conditions.

[tleap2.in](tleap2.in)
```bash
source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams EFZ_H.frcmod
loadoff ligand.lib
complex = loadpdb 1fko_trunc_clean.pdb
solvatebox complex TIP3PBOX 12
addionsrand complex K+ 0
addionsrand complex Cl- 0
saveamberparm complex 1fko_trunc_clean.prmtop 1fko_trunc_clean.inpcrd
savepdb complex 1fko_trunc_param.pdb
quit
```
## 5. Run TLEAP
Run TLEAP to create initial structure files:
```bash
tleap -f tleap.in
tleap -f tleap2.in
```
## 6. Prepare MD Run Scripts
Download all [pmemd_files](pmemd_files.zip) setup files and create bash scripts [run_md.sh](run_md.sh) for running the MD simulation.

Simulation Stages
The MD simulation will undergo the following stages:

Energy Minimization1: The entire system undergoes minimization.


Energy Minimization2: Restraint applied only to the protein backbone.


Energy Minimization3: Restraint applied only to the alpha carbons (Cα) of the protein.


Equilibration0: Without any restraints.


Equilibration1: System is heated from 0K to 310K and undergoes molecular dynamics simulations.


Equilibration2: Equilibrating the system at constant temperature and pressure (NTP ensemble).


Production Molecular Dynamics: System undergoes long molecular dynamics simulations in the NTP ensemble.


### run the [run_md.sh](run_md.sh)  
```bash 
nohup bash run_md.sh &
```
## 7. Analysis
the trajectory is available at 
```
scp -r mathar@altair.dsf.unica.it:/scratch/mathar/{md1.nc,load_vmd.tcl,cpptraj_1.in} .

```



# Reference
This tutorial is adapted from https://ambermd.org/tutorials/basic/tutorial4b/









