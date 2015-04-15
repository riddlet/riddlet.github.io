from bs4 import BeautifulSoup
import urllib2
import datetime
import pandas as pd
import requests

baseurl = 'http://nypost.com/horoscope/'
signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 
         'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

start = pd.datetime(2013, 12, 01)
end = datetime.datetime.today()
rng = pd.date_range(start, end)

scope = []

for sign in signs:
    for day in rng:
        url = baseurl + sign + '-' + day.strftime('%m-%d-%Y') + '/'
        page = requests.get(url)
        if not page.ok:
            continue
        try:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            soup = soup.find('div', 'entry-content')
            soup = soup.find('p').string
            scope.append(soup)
        except:
            print url    

        
