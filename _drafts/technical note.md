---
layout: post
title: Test
---

technical note

prop test versus binomial test.

In some of my recent analyses, I was working with binomial data.  In particular, I had run an experiment in which I had subjects make a judgment on the state of the world.  For simplicity, we’ll pretend that I showed them pictures of irises, or did not show them pictures of irises, and then asked them if that trial contained an iris.

picture of irises

The initial assumption is that I’d be interested in how often they got it right.  And for some of the analyses, I was.  However, a colleague asked not about how often they got it right, but to what extent they were biased in their responding.  What’s the difference?

If I were asking how often my subjects were correct in detecting an iris, I might find that they got it right 100% of the time.  However, that does not mean that they responded perfectly!  To illustrate, let’s create a victor indicating whether I (the experimenter) presented an iris on any given trial.

#1 = iris present, 0 = iris not present
iris <- rbinom(100, 1, prob=.5)

Next we can create a vector which indicates a subject’s response.  If they are responding perfectly, then we would expect these two vectors to be identical, thus:

perfect.subject <- iris

On the other hand, they might detect the iris 100% of the time by a different strategy.  Namely, they could just say ‘iris’ every time.

straightliner <- rep(1, 100).

Both of these subjects correctly say iris 100% of the time that the iris is on the screen:

perfect.table <- table(iris, perfect.subject)
straightline.table <- table(iris, straightliner)

perfect.table[2,2]/perfect.table[2, 2]+perfect.table[2,1]

straightline.table[2]/straightline.table[2]

So, raw accuracy is clearly not a good measure of performance here.  Fortunately, signal detection theory was developed to deal with just this type of scenario.  In particular, one can obtain a measure of bias, often labeled c (for criterion - as in, what is the value of the criterion which divides those instances in which a subject gives one type of response versus the other).  One needs only two numbers for this calculation - the proportion of hits (out of all opportunities for a hit) and the proportion of false alarms (out of all opportunities for a false alarm).  

In the iris example, a hit is defined as any trial in which I presented an iris and the subject responded ‘yes, there’s an iris there’.  A false alarm is defined as any trial in which I presented no iris, but the subject still responded ‘yes, there’s an iris there’.  To obtain the measure of bias, we simply take

-.5 * (z(h) + z(fa))



