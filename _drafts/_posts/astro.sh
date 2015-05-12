#!/usr/bin/python

# Directives
#PBS -N astrology
#PBS -W group_list=yetipsych
#PBS -l nodes=2
#PBS -l mem=128000mb
#PBS -l walltime=12:00:00
#PBS -M tar2119@columbia.edu
#PBS -m abe
#PBS -V

# Set output and error directories
#PBS -o localhost:/vega/psych/users/tar2119/riddlet.github.io/out
#PBS -e localhost:/vega/psych/users/tar2119/riddlet.github.io/err
echo '2 nodes, 128000mb, walltime 12hrs'
date

module load anaconda/2.7.8
python -W ignore astrology.py


# Print date and time
date

# End of script