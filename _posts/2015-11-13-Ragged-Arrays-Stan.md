---
title: "Ragged arrays in Stan"
layout: post
---

[Stan](http://mc-stan.org/) is a probabalistic programming language that helps to simplify the goal of fitting statistical models to probability distributions. In other words, it's a modeling language for Bayesian data analysis. To fit a model in Stan, you need to first decide on the model (i.e. what is the data generation process?), then translate that into Stan code.

The Stan [users manual](http://mc-stan.org/documentation/) is pretty comprehensive. It has example code for models fit to all types of data analysis problems. Also, the developers are very active on the Stan users mailing list. So if you have problems, it seems as though there are ample resources to help you through them. One such problem that I encountered was how to deal with ragged arrays.

What are ragged arrays? It arises in an analytic situation where you have different numbers of observations for each level of a given grouping. In my situation, this was different numbers of observations for different individuals. For instance:

| Sub | Grade | Grade | Grade | Grade | Grade |
|-----+-------+-------+-------+-------+-------|
| 1   |  4.0  |  4.0  |  4.0  |  4.0  |  4.0  |
| 2   |  3.2  |  3.1  |       |       |       |
| 3   |  3.8  |  4.0  |  2.9  |  3.3  |       |
| 4   |  2.7  |  2.5  |  2.3  |       |       |

Each of our subjects here has different numbers of observations. After lamenting Stan's inability to automatically handle this, the developers provide the following syntax as a suggested work around:

{% highlight c++ %}
data {
int<lower=0> N; // # observations
int<lower=0> K; // # of groups
vector[N] y; // observations
int s[K]; // group sizes
...
model {
int pos;
pos <- 1;
for (k in 1:K) {
segment(y, pos, s[k]) ~ normal(mu[k], sigma);
pos <- pos + s[k];
}
{% endhighlight %}

They key bit there comes from the last three lines. It seems like they're breaking `y` into individual-level chunks and stating that the observed values are sampled from the individual-level estimate of `mu`. I tried implementing something similar (using the segment function) and was not able to get it to run. Instead, I used a different trick that seems to accomplish the same thing.

Here's the model block:

{% highlight c++ %}
model {
  vector[n] nu;
  int pos;
  int target;
  pos <- 1;
  target <- pos;
  sigma ~ cauchy(0,5);
  sigma_mu_int ~ cauchy(0,5);
  sigma_mu ~ cauchy(0,5);
  mu_time ~ normal(0,10);
  mu_int ~ normal(0,10);


  for (i in 1:p){
  	target <- target+s[i];
    intercept[i] ~ normal(mu_int, sigma_mu_int);
  	b_time[i] ~ normal(mu_time, sigma_mu);
  	while (pos < target){
  		nu[pos] <- intercept[i] + b_time[i]*t[pos];
  		pos <- pos+1;
  	}
  }
  y ~ normal(nu, sigma);
}
{% endhighlight %}

So, let's look at it from the inside out. First, the observed data, `y`, are sampled from a normal centered on `nu` with variance `sigma`. We define nu for each participant with this line `nu[pos] <- intercept[i] + b_time[i]*t[pos];`. This is nested inside a while loop so that we have a value for each time point for each individual, regardless of how many observations that person has. This value is a function of an intercept and a slope coefficient for time, each of which are subject-specific and are sampled from their respective prior distributions (`mu_time ~ normal(0, 10)` and `mu_int ~ normal(0,10)`). This runs! Also, the parameters make sense and look about right.

If there's a way of getting this to run with the segment function, I'd like to see it. I couldn't make it happen to save my life.