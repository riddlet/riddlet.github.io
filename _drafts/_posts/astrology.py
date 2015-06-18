from bs4 import BeautifulSoup
import urllib2
import datetime
import pandas as pd
import requests
import numpy as np
import os

baseurl = 'http://nypost.com/horoscope/'
signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 
         'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

start = pd.datetime(2013, 12, 01)
end = datetime.datetime.today()
rng = pd.date_range(start, end)

scope = []
zodiac = []
pub_date = []
sign = 'pisces'

for sign in signs:
    print sign
    for day in rng:
        url = baseurl + 'pisces' + '-' + day.strftime('%m-%d-%Y') + '/'
        page = requests.get(url)
        if not page.ok:
            continue
        try:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            soup = soup.find('div', 'entry-content')
            soup = soup.find('p').string
            scope.append(soup)
            zodiac.append(sign)
            pub_date.append(day.strftime('%m-%d-%Y'))
        except:
            scope.append(np.nan)   
            zodiac.append(sign)
            pub_date.append(day.strftime('%m-%d-%Y'))
            
df = pd.DataFrame({'horoscope' : scope,
                   'zodiac' : zodiac,
                   'pub_date' : pub_date})
                   
df.to_csv('pisces.csv', sep='|')

scopes = []
for f in os.listdir('./../data/horoscopes'):
    df=pd.read_csv('./../data/horoscopes/' + f, sep='|')
    df['astrosign'] = f
    scopes.append(df)
frame=pd.concat(scopes)

for i, s in enumerate(df.astrosign):
    df.zodiac.iloc[i] = s[:-4]

df = df.drop('astrosign', 1)
df = df.drop('Unnamed: 0', 1)

df.to_csv('astrosign.csv', sep='|')