# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#
# First, I import the libraries
import pandas as pd
import numpy as np
import re
import glob
import os
import matplotlib
from pylab import *

#
# Next, I extract the files, and add what year they came from
pathdir = os.path.dirname(os.path.abspath('__file__'))
pathdir = os.chdir('..')
files = glob.glob('data/Scopus-*.csv')
data = pd.DataFrame()
for f in files:
    yearfile = pd.read_csv(f, skiprows=7)
    year = re.search('[1-2][0-9][0-9][0-9]', f)
    yearfile['Year'] = year.group(0)
    data = pd.concat([data, yearfile])
   
#
# Rename the columns for clarity
data.rename(columns={'SOURCE TITLE':'Source Title', 'Unnamed: 1':'Papers'}, 
            inplace=True)

#
# Remember, we're explaining this weird jump:
papersbyyear = data.groupby('Year')['Papers'].sum()
papersbyyear.plot()

#
# For the next set of tricks, it would be good to see if there were any jumps 
# in the number of journals for each year.
titlesbyyear = data.groupby('Year')['Source Title'].nunique()
titlesbyyear.plot(ylim=(155,165))

#
# Nothing there I guess.  We can look to see which journals saw the biggest 
# increase from 1995 to 1996
datawide = data.groupby(['Year', 'Source Title']).Papers.sum().unstack('Year')
datawide['Change'] = datawide['1996']/datawide['1995'] 
datawide.head()
datawide.sort = datawide.sort('Change', ascending=0)

    