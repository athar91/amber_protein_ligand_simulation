#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
source /etc/modules.sh
module load amber20
EXE=$(which pmemd)
DIR=.
PARM=$DIR/1fko_trunc_clean.prmtop

################
#1
NAME=opt_restr_all
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$DIR/1fko_trunc_clean.inpcrd
RESTART=rest_${NAME}.rst7
REF=$DIR/$INITCRD
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY -ref $REF

################
#2
NAME=opt_restr_backbone
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
REF=$INITCRD
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY -ref $REF

################
#3
NAME=opt_restr_CAs
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
REF=$INITCRD
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY -ref $REF

################
#4
NAME=opt
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
REF=$INITCRD
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY

################
#5
NAME=anneal
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
REF=$INITCRD
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY
#mpirun -np 2 pmemd.MPI -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY

################
#6
NAME=equilibrate_NTP
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
REF=$INITCRD
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc 
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY
#########
#7
NAME=md1
IN=${NAME}.pmemd
OUT=${NAME}.out
INITCRD=$RESTART
RESTART=rest_${NAME}.rst7
COORD=${NAME}.nc
ENERGY=${NAME}.energy

$EXE -O -i $IN -o $OUT -p $PARM -c $INITCRD -r $RESTART -x $COORD -e $ENERGY


