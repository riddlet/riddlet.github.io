---
title: "Scraping Horoscopes"
layout: post
---

Astrology drives me bananas. Don't get me wrong - I understand why people enjoy
it, and why someone might check their horoscope regularly. People do lots of
weird things, but there's always some underlying set of psychological
explanations for these behaviors. For the astrologically inclined, the idea that
the world is governed by the positions of planets and stars is a comforting one.
At least, it's a hell of a lot more comforting than the truth - that the world
is a pretty chaotic place, and trying to understand it or make specific
predictions (about the behaviors of individual agents, for example) is close to
impossible.

But *actually* buying into it? And actively arguing for their veracity? Come on.

Anyway, I wanted to practice doing some web scraping and some simple modeling of
text data. This post is about the former. I thought astrological forecasts,
being published daily, would make a great thing to look at. It was a little
difficult to find historical astrological forecasts. I guess this shouldn't be
surprising. How many horoscope readers really want to go back to last week's
horoscope to see if the predictions came true? Probably vanishingly few.

Fortunately, the [New York Post](http://nypost.com/) does something other than
make [awesome puns](http://www.mandatory.com/2012/12/03/the-most-ridiculous-new-
york-post-headlines-over-the-years/) - they have their horoscopes archived going
back to at least December 2013. Even better, they do it with nicely formatted
URLs. For example, here's the urls for Aries from 12/01/2013 to 12/05/2013

http://nypost.com/horoscope/aries-12-01-2013/
http://nypost.com/horoscope/aries-12-02-2013/
http://nypost.com/horoscope/aries-12-03-2013/
http://nypost.com/horoscope/aries-12-04-2013/
http://nypost.com/horoscope/aries-12-05-2013/

Given those five examples, I'm sure you can guess what the link is for any given
horoscope on any date between 12/01/2013 and the present day. Because they're so
regularly formatted, that means that it wont be hard to write a little script to
go to each webpage and pull out the information we're interested in.

There's two other considerations we'll need here. First, if you've spent much
time surfing the internet, you know that sometimes pages don't work. You have to
refresh for the page to load, or the page is inexplicably removed. If I'm going
to automatically grab text from over 6000 individual pages (12 signs * ~1.5
years of horoscopes), I need to build in something to account for the fact that
not every page I visit will be a success.

Second, once we successfully visit a page, I'm not going to be interested in
*all* of it. There's a lot of advertisements and links to other punny articles
and buttons to like stuff or subscribe to something and all the glorious,
chaotic noise that is the internet. I need some way of wading through this mess
and pulling out only the information I want.

To solve the former problem, we'll turn to the python module
[requests](http://docs.python-requests.org/en/latest/). This module gives us a
nice way to ping a webpage and see if it answers back.


    import requests
    url = 'http://nypost.com/horoscope/aries-12-01-2013/'
    page = requests.get(url)

Now, this new variable, page, has a method that tells us if the page responded
appropriately:


    page.ok




    True



If, on the other hand, we try to visit a bad page, we get something slightly
different:


    url = 'http://nypost.com/horoscope/aries-12-01-2015/' #doesn't exist because it hasn't happened!
    page = requests.get(url)
    page.ok




    False



Great! We've solved the first problem. For the second, we need two things.

First, we need to know what part of the webpage we want. Because most of the
stuff you see on the internet is composed of rigidly constructed html, this
means that we can use that structure to automatically select the information we
want. There's two ways I do this - [selector gadget](http://selectorgadget.com/)
or using Chrome's developer tools (open chrome - go to View -> Developer ->
Developer Tools). If we look at our horoscope pages, we see that the content
we're interested in (the text of the horoscope) is contained within an element
'p', which is itself contained within an element 'div' with the label 'entry-
content'.

Now that we know where our wanted content is, we can use the wonderfully named
[beautiful soup](http://www.crummy.com/software/BeautifulSoup/) module to grab
the information we want.

*Confession: These two things always involve a lot of trial-and-error for me.
I'm no expert on this stuff. I just use them as tools to greater ends*


    import urllib2
    from bs4 import BeautifulSoup
    url = 'http://nypost.com/horoscope/aries-12-01-2013/'
    content = urllib2.urlopen(url).read() #Get the actual html content of the webpage
    soup = BeautifulSoup(content)
    soup = soup.find('div', 'entry-content')
    soup = soup.find('p').string
    print soup

    You’re not the sort to play safe and even if you have been a bit more cautious than usual in recent weeks you will more than make up for it over the next few days. Plan your new adventure today and start working on it tomorrow.


There we are! That's the stuff we wanted! Now we can put all this stuff together
to scrape all the data we want. I tried to do this a couple of times, but the
tool broke down after a couple of hours, so instead of doing it in a big loop
like I pasted below, I did it sign-by-sign over the course of a couple of days.

Anyway, here's the whole thing. If you want the compiled data, you can find it
in pipe-delimited format
[here](http://sparrowlab.psych.columbia.edu/tar/data/astrosign.csv). Next time,
I'll do some actual work with these data.


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
    
    for sign in signs:
        print sign
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
                zodiac.append(sign)
                pub_date.append(day.strftime('%m-%d-%Y'))
            except:
                scope.append(np.nan)   
                zodiac.append(sign)
                pub_date.append(day.strftime('%m-%d-%Y'))
                
    df = pd.DataFrame({'horoscope' : scope,
                       'zodiac' : zodiac,
                       'pub_date' : pub_date})
                       
    df.to_csv('astroscope.csv', sep='|')
