---
layout: post
title: Some tweaks to the workflow
---

I've found Jekyll to be a good mechanism for publishing these thoughts, code & analyses.  However, every now and then I run into a problem which requires a bit of tweaking.  For instance, getting latex to render with the Rmarkdown -> jekyll -> github pages workflow turned out to be a bit of a hassle.  Here's what I ended up doing:

###### 1.  .Rmd -> .md

I used the `KnitPost` function I found [here][ref1].  It has worked beautifully so far.  We'll see how it holds up in the long-term.

###### 2.  Latex support?

This led to output which either just displayed the latex directly, as follows:

<div>\sigma = \sqrt{\frac{n_1 \sigma_1^2 + n_2 \sigma_2^2 + n_1(\mu_1 - \mu)^2 + n_2(\mu_2 - \mu)^2}{n_1 + n_2}</div>

Or didn't display at all, depending on how, exactly, I adjusted the site settings (as found in the _layouts or _includes directories; or in the _config.yml file).  

The solution took a bit of digging around, but eventually after looking around [Carl Boettiger's][ref2] site for long enough, I was able to figure out how this works.  To the `default.html` file in the _layouts folder, I added:

{% highlight html %}
<script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
{% endhighlight %}

And that seems to have taken care of the issue.  What we're doing there seems to be just linking the mathjax display library directly from the mathjax site.

**Plug:**  [Carl Boettiger's][ref2] site is really fascinating.  I could (and very well might) spend quite a while digging around in there.  Lots of information to digest, but it seems to be a pretty great approach to science.

    
[ref1]: <http://www.jonzelner.net/jekyll/knitr/r/2014/07/02/autogen-knitr/>
[ref2]: <http://www.carlboettiger.info>