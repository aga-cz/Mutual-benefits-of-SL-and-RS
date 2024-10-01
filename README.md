This repository contains code for the paper `Mutual benefits of social learning and algorithmic mediation for cumulative culture' by Agnieszka Czaplicka, Fabian Baumann and Iyad Rahwan.

## MODEL EXECUTION

The code implementing agent-based model to reproduce results from the paper was written in C.
``` r
# in terminal use gcc to compile the file (modelQinn.c) and make an executable (modelQinn) 
gcc -Wall -o modelQinn modelQinn.c -lm
```
Example execution of modelQinn is given is bash scripts. To run the scripts in terminal type:
``` r
chmod +x script_runQinn.sh
./script_runQinn.sh
```

## PLOTS

Scripts for visualization are written in Python. 
``` r
python3 plots_ER.py
```
