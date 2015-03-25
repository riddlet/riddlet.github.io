from bs4 import BeautifulSoup
import urllib2
import datetime
import pandas as pd

start = pd.datetime(2013, 12, 01)
end = datetime.datetime.today()
rng = pd.date_range(start, end)
for day in rng:
	datetime.datetime.strptime(day, '%Y-%M-%d').strftime('%M-%d-%Y')


url = 'http://nypost.com/horoscope/sagittarius-01-24-2014/'

content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content)

soup = soup.find('div', 'entry-content')

soup = soup.find('p').string

\