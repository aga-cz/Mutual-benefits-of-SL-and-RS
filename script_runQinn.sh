#!/bin/bash

Q=200 #number of realizations

N=100 #system size

X=100 #num of items
L=1000 #budget
S=5 #cost of SL
I=10 #cost of innovation
R=1 # cost of recommendation

dirP="N${N}X${X}Ci${I}Cs${S}Cr${R}_avg_inn"
mkdir $dirP

out_dir_t="${dirP}/"



for r in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
	for p in 0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
	do
	
		./modelQinn $N $p $X $L $S $I $R $r $Q $out_dir_t
	done
done  
