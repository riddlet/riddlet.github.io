from bs4 import BeautifulSoup
import urllib2
import datetime
import pandas as pd

baseurl = 'http://nypost.com/horoscope/'
signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 
         'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

start = pd.datetime(2013, 12, 01)
end = datetime.datetime.today()
rng = pd.date_range(start, end)
for day in rng:
    for sign in signs:
        url = baseurl + sign + '-' + day.strftime('%m-%d-%Y') + '/'
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        soup = soup.find('div', 'entry-content')
        soup = soup.find('p').string



url = 'http://nypost.com/horoscope/sagittarius-01-24-2014/'

content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content)

soup = soup.find('div', 'entry-content')

soup = soup.find('p').string

\