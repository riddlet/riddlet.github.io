---
title: "The power and pain of regular expressions"
layout: post
---

When working with unstructured text data, you often end up looking for specific string patterns. Maybe you want to search a document for phone numbers, or you might look for emoticons or web addresses. Maybe you have to search through 200mb of emails looking for something formatted like an address to prevent a murder (or maybe that's only ever happened to [Randall Munroe](https://xkcd.com/208/)). All of these instances are examples of string data that consist of a specific pattern, but with variable content. Since the content is different, it obviously isn't possible to search for these constructions using the normal approach. What's an analyst to do?

Regular expressions to the rescue! Regular expressions are a formal way of searching for string patterns. They're extraordinarily useful for all kinds of tasks. In the last few months, I've used them to:

- Break up information stored in a series of filenames: 

{% highlight text %}
1059_c_10-26-2004_7  
1060_c_10-26-2004_7
{% endhighlight %}
- Extract the number from a series of observations:  
{% highlight text %}
time_7  
time_2  
time_1  
time_1  
{% endhighlight %}

- Find all instances of a specific word in a raw .txt file and get the number that occurs immediately afterwards:  
{% highlight text %}
...topic 7...  
...topic 27...  
...topic 18...  
{% endhighlight %}

Most recently, I've been using on some essays that have been marked for incorrect spelling and grammar. I use the regular expressions to detect the edits, and then replace the original text with the suggested edits. For instance given a sentence like:

```
Politics would be very important for people who are intrested in being a lawer.
```

It has been marked as:

```
Politics would be very important for people who are intrested @interested@ in being a lawer. @lawyer.@
```

Using regular expressions, I was able to turn that into this:

```
Politics would be very important for people who are interested in being a lawyer.
```

What's especially cool about these constructions is that they can be self-referential. What do I mean by that? Well, Looking at the previous sentence, I want to be able to find all the spots in which a word that has and `@` symbol at the front at the back. But I don't want just that, I also want to be able to find the previous word. In other words, just finding `@interested@` is no good. I need to be able to find `intrested @interested@`. Finally, I need to be able to replace the entire thing with a subpart - whatever is between the `@` symbols.

```
essaytext <- gsub("\\w*'?\\w*['.,]?\\s?@(.*?)@", '\\1', essaytext)
```

UGH. BLECH. UGLY. This is the price you pay for super flexibility I guess. The syntax for this is just absolutely awful to look at. No matter how useful I know regular expressions to be, I never jump right into using them. I inevitably waste about 20 minutes trying to find some other way of doing it because I find the syntax just so god awful.

Let's break that first bit up just a little bit. Building this thing up a little bit at a time, we have `@(.*?)@` towards the end of that first argument. So, we're looking for a pattern that comes between two `@` symbols. Here, `.` is a wildcard character. That means it matches anything! `*` is a quantifier. It means "zero or more times". So we're matching the wildcard character zero or more times. Finally, we have a `?`. This means to turn what is an eager matching system into a lazy match. Without the question mark, instead of just matching `@interested@`, this system would match `@interested@ in being a lawer. @lawyer.@`, which is not exactly what we want. We also wrap this entire middle bit (between the `@` symbols) in parentheses. This makes it a 'capturing group'. Any groups that we capture, we can re-use, or refer to within the regular expression. 

In front of that we have some stuff that's designed to capture a word, and includes a system for dealing with words like doesn't or you're that feature an apostrophe.

The next argument in the gsub command is also a regular expression. `\\1` refers to the first capture group. In the regular expression we I built, there is only one capture group - the one in between the `@` symbols. So, the entire thing gets replaced with whatever comes between those symbols. 

There are a few other types of edits that I had to deal with. Writing these strings, and learning about the self-referential abilities of regular expressions gave me a new appreciation for them.

But I still don't have to like that syntax.


