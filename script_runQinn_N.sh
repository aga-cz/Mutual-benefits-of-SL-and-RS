#!/bin/bash

Q=200 #num of realizations

p=1.0 #network density
r=0.0 #recommendation prob
X=100 #num of items
L=1000 #budget
S=5 # cost of social learning
I=10 #cost of innovation
R=1 #cost of recommendation

dirP="N${N}X${X}Ci${I}Cs${S}Cr${R}_N"
mkdir $dirP

out_dir_t="${dirP}/"



for N in 10 20 50 100 200 500 1000
do
	./modelQinn_N $N $p $X $L $S $I $R $r $Q $out_dir_t
done  
