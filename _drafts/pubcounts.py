# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import re
from ggplot import *
import glob

files = glob.glob('/Users/triddle/Documents/riddlet.github.io/_drafts/data/Scopus-*.csv')
data = pd.DataFrame()
for f in files:
    yearfile = pd.read_csv(f, skiprows=7)
    year = re.search('[1-2][0-9][0-9][0-9]', f)
    yearfile['Year'] = year.group(0)
    data = pd.concat([data, yearfile])
    
data.rename(columns={'SOURCE TITLE':'Source Title', 'Unnamed: 1':'Papers'}, 
            inplace=True)

plot = ggplot(data, aes(x='Year', y='Papers', color='Source Title')) +\
    geom_line(alpha=0.5)

fig = plot.draw()
