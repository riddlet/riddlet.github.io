---
layout: post
title: "De-identifying"
---



A colleague of mine is collecting longitudinal data on social networks.  To do this, she's asking everyone in the study who their friends are.  Thus, her participants are providing her with a series of names at regular time intervals.  Unfortunately, this poses a few problems.

**1.  The data are not deidentified.**  When working with data, it's almost always a problem when you see people's actual names next to other information about them.  All identifying information should be stripped.

**2.  People provide partially matching names.**  Sometimes, when someone tells you that they are friends with *'Jane Doe'*, you later find that this person's real name is *'Janet Doe'*.  

To solve these problems, she wondered if it were possible to create a function which takes, as an input, a series of individual names and ID numbers, as well as a series of names provided by the participants, and returns the latter series of names, converted to id numbers.

In other words, if you have one file which has names and ID numbers like this:


{% highlight r %}
reference <- data.frame(name=(c("Margaret Mead", "Wilhelm Wundt", "Marie Curie",
                                "David Marr", "Kenneth Clark", "Leonardo da Vinci")),
           id=c(1001, 1002, 1003, 1004, 1005, 1006), stringsAsFactors=F)
reference
{% endhighlight %}



{% highlight text %}
##                name   id
## 1     Margaret Mead 1001
## 2     Wilhelm Wundt 1002
## 3       Marie Curie 1003
## 4        David Marr 1004
## 5     Kenneth Clark 1005
## 6 Leonardo da Vinci 1006
{% endhighlight %}

And then a second vector of names that you'd like to replace with id numbers, where possible:


{% highlight r %}
to.replace <- c('Barbara McClintock', 'Ricky Feynman', 'Marie Curie', 
                'Will Wundt', '', NA, 'marge mead', 'Florence Nightingale', 
                NA, 'Ken Clark', 'Ibn al-Haytham', 'Leo da Vinci')
{% endhighlight %}

Can we get a function which accomplishes this?

Obviously, the *real* question is not whether we can, but rather how we can do it.

I've included below the function that accomplishes this.  What we're doing is matching based on the first few letters of the person's first name, paired with the last name (or last $$n$$ names in cases where someone has more than 1 'name' after their first), and then replacing these with the corresponding id numbers. 

For instance, matching based on the first 3 letters in the first name:


{% highlight r %}
replacenames(reference$name, reference$id, to.replace, 3)
{% endhighlight %}



{% highlight text %}
## Joining by: short
{% endhighlight %}



{% highlight text %}
##  [1] "Barbara McClintock"   "Ricky Feynman"        "1003"                
##  [4] "1002"                 ""                     NA                    
##  [7] "1001"                 "Florence Nightingale" NA                    
## [10] "1005"                 "Ibn al-Haytham"       "1006"
{% endhighlight %}

Versus the first 4 letters:


{% highlight r %}
replacenames(reference$name, reference$id, to.replace, 4)
{% endhighlight %}



{% highlight text %}
## Joining by: short
{% endhighlight %}



{% highlight text %}
##  [1] "Barbara McClintock"   "Ricky Feynman"        "1003"                
##  [4] "Will Wundt"           ""                     NA                    
##  [7] "1001"                 "Florence Nightingale" NA                    
## [10] "Ken Clark"            "Ibn al-Haytham"       "Leo da Vinci"
{% endhighlight %}

3 grabs more of them, so why would we ever want 4?  This helps in case you happen to have a Rick Williams and a Rich Williams, or something of the sort..

And the function itself below.  Note that plyr is a dependency - make sure you've got that package installed if you want this to work:


{% highlight r %}
replacenames <- function(namesRef, id, namesReplace, firstNameLetters) {  
  #This function takes as input a vector of names (namesRef), a vector of id
  #numbers associated with those names (id), a vector of names to replace with those
  #id numbers (namesReplace) wherever a match is found, and a value indicating 
  #how many letters of the first name one should match to (e.g. a 2 will take 
  #'Jane Doe' and match all instances of 'Ja Doe')
  
  library(plyr)
  
  #split into separate names
  refSplit <- strsplit(namesRef, ' ')
  
  # get first 'word' (as defined by where there are spaces)
  ref.first <- substr(unlist(lapply(refSplit, '[[', 1)), 1, firstNameLetters) 
  #get the remaining 'words' (i.e. 2nd, 3rd, 4th names, etc.)
  last<-lapply(refSplit, '[', -1) 
  last<-unlist(paste(last))
  #All this removes weird encoding stuff from the letter string
  last<-gsub('c\\(\\"', '', last)
  last<-gsub('\\\", \\"', ' ', last)
  last<-gsub('\\\")', '', last)
  #new var:  shortened version of their name
  short.full <- tolower(paste(ref.first, last))
  
  
  #split each name into first and last
  repSplit <- strsplit(as.character(namesReplace), ' ')
  #only look at the ones with more than one name listed
  moreThanOneName<-repSplit[lapply(repSplit, length)>1]
  
  #newvars: first name, last name, shortened version of name, and full name
  #*** substr().  see above
  rep.first<-substr(tolower(unlist(lapply(moreThanOneName, '[[', 1))), 1, 
                    firstNameLetters)
  rep.last<-lapply(moreThanOneName, '[', -1)
  rep.last<-unlist(paste(rep.last))
  rep.last<-gsub('c\\(\\"', '', rep.last)
  rep.last<-gsub('\\\", \\"', ' ', rep.last)
  rep.last<-gsub('\\\")', '', rep.last)
  rep.short <- paste(rep.first, tolower(rep.last), sep=' ')
  rep.full <- paste(tolower(unlist(lapply(moreThanOneName, '[[', 1))), 
                    rep.last, sep=' ')
  
  #dataframe, including the row that each name was extracted from (loc)
  df.1<-data.frame(first=rep.first, last=rep.last, short=rep.short, 
                   loc=which(lapply(repSplit,length)>1))
  
  #this joins them by the common column - shortened version of the name, 
  #getting rid of NAs
  df.2<-na.omit(join(df.1, data.frame(short=short.full, id=id)))
  
  #get the column from Friends, and turn it into char (from a factor)
  namesReplace<-as.character(namesReplace)
  
  #insert the PPID as characters (instead of factors) into the column (in the spot where loc indicates)
  namesReplace[df.2$loc]<-as.character(df.2$id)
  
  #replace the original column
  return(namesReplace)
  
}
{% endhighlight %}

Happy de-identifying!
