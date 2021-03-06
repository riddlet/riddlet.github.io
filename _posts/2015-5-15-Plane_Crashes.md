---
title: "Plane crashes"
layout: post
---


Someone recently suggested to me that it seems as though there have been more plane crashes than typical in recent months. I disagreed with this assessment, and said that one reason it seemed that way was because the crashes we've seen recently have [been](http://en.wikipedia.org/wiki/Germanwings_Flight_9525) [tragically](http://en.wikipedia.org/wiki/Malaysia_Airlines_Flight_370) [salient](http://en.wikipedia.org/wiki/Malaysia_Airlines_Flight_17).

Fortunately, only a couple of days after this conversation, I found a [nifty little r function](https://github.com/philjette/CrashData) written by Phil Jette which scrapes a website that logs airline crashes.  After obtaining the data, I thought I'd look to see if there was any support for the idea that there have been an inordinate number of crashes recently.  Here's a line graph by year:


{% highlight r %}
df <- compiledData %>%
  group_by(crashYear) %>%
  summarise(crashes = length(crashYear)) %>%
  ungroup()
df$crashYear <- as.numeric(df$crashYear)

library(ggplot2)
ggplot(df) + 
  geom_line(aes(x=crashYear, y=crashes, group=1), color='#88301B', size=1) + 
  scale_x_continuous(breaks=seq(1950, 2015, 5)) +
  theme_bw()
{% endhighlight %}

![center](/../figs/planes/unnamed-chunk-2-1.png) 

There's still more of 2015 to go.  What if we extrapolated through the end of the year, given how many crashes have been observed so far?  Today is May 15th.


{% highlight r %}
start <- '01-01-2015'
now <- '05-15-2015'
as.Date(now, format='%m-%d-%Y') - as.Date(start, format='%m-%d-%Y')
{% endhighlight %}



{% highlight text %}
## Time difference of 134 days
{% endhighlight %}

What proportion of the year is that?


{% highlight r %}
134/365
{% endhighlight %}



{% highlight text %}
## [1] 0.3671233
{% endhighlight %}

Okay, so let's extrapolate whatever number of crashes we've seen so far through the rest of the year and replot with the new value.


{% highlight r %}
year.complete <- 134/365
year.remaining <- 1-year.complete
estimated.total <- df$crashes[which(df$crashYear == 2015)]/year.remaining
df$crashes[which(df$crashYear == 2015)] <- estimated.total

ggplot(df) + 
  geom_line(aes(x=crashYear, y=crashes, group=1), color='#88301B', size=1) + 
  scale_x_continuous(breaks=seq(1950, 2015, 5)) +
  theme_bw()
{% endhighlight %}

![center](/../figs/planes/unnamed-chunk-5-1.png) 

Caveats about the data source apply, but I think it's safe to say that we're not seeing a dramatic increase in plane crashes these days.  Especially since all of this is just raw counts and doesn't take into account the number of flights each year - something I'm sure is on an upward trajectory.


