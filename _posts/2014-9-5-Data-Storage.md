---
layout: post
title: Thinking about Data Storage
---

I've just started a post-doc, and the things I've had to think about so far have been much different from many of the problems I encountered while pursuing the PhD.  Given that a large part of this project is something similar to a meta-analysis, one problem I've had to deal with almost immediately is to spend some time thinking about what sorts of files and what kind of file structure I should work with.

As a grad student, I began life working with an array of spss, excel, matlab, and stata files.  However, that quickly grew tiresome.  Sometime in my second year, I transitioned to using strictly a .csv filetype.  Along with my increasing (soon to be full) reliance on R for all data munging and analysis, this streamlined my workflow and allowed me to pull data from a variety of sources without worrying about findings ways to translate between file types.

Now, however, I’m running up against a new set of challenges - some of which I saw coming toward the end of my PhD, when I started seriously toying around with text as data.  Specifically, within text, there are all kinds of commas and quotes and tabs and such which are typically used as delimiters in data file types (i.e. csv = comma separated value, tsv = tab separated value).  Given that I’ll work with this type of data heavily in my postdoctoral research, I think its time to settle on a new data storage system.

My initial idea is to use xml to store the data.  I’ve settled on this for a variety of reasons:

1.  In my early struggles during the PhD with text data, I eventually found that a simple xml file, which stored the text generated from each participant allowed me to easily get around the delimiter problem, and I could easily read it into R for parsing.
2.  XML should allow a fair amount of flexibility for storing data from studies which will frequently have dramatically different data.  What I mean here is that since I’m compiling data from many studies, some of which feature vast, longitudinal data, including multiple writing samples and essays from a given individual, along with varying types of demographic data and a currently unknown array of outcome measures and other covariates, I think XML should allow me to centralize all this information with limited overhead.  This is especially true in light of the fact that….
3.  I really have no idea how I will receive all this data.  I’ve got a diligent research assistant currently going through our data to do a full accounting of what we’ve got, where, and in what formats.  It seems like the stuff in our lab is all stored as a series of excel documents.  However, this may not be the case in other labs.
4.  One of the PIs on the grant whose primary area of research is in natural language processing seemed to implicitly endorse this plan when I mentioned off-hand that I might store the data in an xml file.

I’ve done a little bit of digging around, and while it seems that there are some downsides to using xml as a method of storing data (e.g. verbose, inefficient), I don’t think those apply as strongly in my case, as I’m not going to be dealing with a massive dataset (a few thousand individuals at most, each with a range of outcome and demographic variables - somewhere around 100-200?).  Also, my data is static - I’m not collecting any new data at the moment, and so won’t have to deal with injecting new stuff into the file, once it is built.  I think the most likely plan is to store all essays and some identifying information in an xml file (e.g. date of writing, experimental condition, etc), and the other data, including primary dependent variables and all covariates, in csv file.

Going with this plan should allow me to share the data with my collaborators in a straightforward manner, including the scripts used to parse and anaylze the textual data.

However, I haven’t made any xml files yet!  So I would certainly be interested if there’s a better approach than what I’ve outlined here, given my constraints and goals.



