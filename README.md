# Molecular Dynamics Simulation Tutorial

This tutorial guides you through the process of setting up and running a molecular dynamics (MD) simulation for a protein-ligand complex using the AMBER molecular dynamics software suite.

## Introduction
In this tutorial, we will simulate the prescription drug Sustiva (Efavirenz) in complex with HIV-1 REVERSE TRANSCRIPTASE. Efavirenz is a human immunodeficiency virus type 1 (HIV-1) specific, non-nucleoside, reverse transcriptase (RT) inhibitor marketed by Bristol Myers Squibb for controlling the progression of HIV infection in humans.

## Test Environment
The tutorial assumes the following test environment:

```bash
mathar@freddie:~/cheetah/andrea_files/try/tutorial8 

```
## Steps

## 1. Download PDB Structure
Download a PDB structure file for your protein-ligand complex. In this tutorial, we'll use the example structure `1fko.pdb`.


## 2. Prepare Protein Structure
Open the PDB structure in VMD and save only the protein coordinates using the following VMD selection:
(chain A and resid 1 to 243 or resname EFZ)
Save the protein structure as 1fko_trunc.pdb.

## 3. Clean and Prepare Ligand
Clean the ligand structure using pdb4amber, grep, reduce, and antechamber. Run the following commands:

pdb4amber
```bash
pdb4amber -i 1fko_trunc.pdb -o 1fko_trunc_clean.pdb --add-missing-atoms --no-reduce-db --most-populous
```


grep EFZ
```bash
grep EFZ 1fko_trunc_clean.pdb > EFZ.pdb
```


reduce
```bash
reduce EFZ.pdb > EFZ_H.pdb
```
 antechamber
```bash
antechamber -i EFZ_H.pdb -fi pdb -o EFZ_H.mol2 -fo mol2 -c bcc -s 2
```
parmchk2
```bash
parmchk2 -i EFZ_H.mol2 -f mol2 -o EFZ_H.frcmod
```
# 4. Create Leap Input Files
Create two TLEAP input files (tleap.in and tleap2.in) with the provided content.

tleap.in
```bash
source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.tip3p
EFZ = loadmol2 EFZ_H.mol2
check EFZ
loadamberparams EFZ_H.frcmod
saveoff EFZ EFZ.lib
saveamberparm EFZ ligand.prmtop ligand.inpcrd
quit
```
tleap2.in
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
Create bash scripts (run_md.sh and plain_md) for running the MD simulation.

Simulation Stages
The MD simulation will undergo the following stages:

Energy Minimization1: The entire system undergoes minimization.
Energy Minimization2: Restraint applied only to the protein backbone.
Energy Minimization3: Restraint applied only to the alpha carbons (Cα) of the protein.
Equilibration0: Without any restraints.
Equilibration1: System is heated from 0K to 310K and undergoes molecular dynamics simulations.
Equilibration2: Equilibrating the system at constant temperature and pressure (NTP ensemble).
Production Molecular Dynamics: System undergoes long molecular dynamics simulations in the NTP ensemble.


run_md.sh
```bash 
run_md.sh
```









