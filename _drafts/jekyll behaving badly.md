---
layout: post
title: Jekyll behaving badly
---

I use a combination of things to build this blog.  I write the posts in [markdown](http://daringfireball.net/projects/markdown/) and then use [jekyll](http://jekyllrb.com/) and [github pages](https://pages.github.com/) to publish.  I recently encountered an issue I suspect may be a bug that occurs when jekyll parses markdown to html.

Here's the markdown.  I'm using some html to color specific words:

	Write some stuff here.  Then I continue on and want to add some colorful font on a new line:

	<font color = '#FFD441'>This </font>should work<font color = '#584CD5'> just</font> <font color = '#FFB441'>fine</font>.

and here's the jekyll parse:

	Write some stuff here.  Then I continue on and want to add some colorful font on a new line:

	<font color = '#FFD441'>This </font>
	<p>should work<font color = '#584CD5'> just</font> <font color = '#FFB441'>fine</font>.</p>

The words get colored fine, but I get this weird extra `<p>` tag, which means that it gets rendered like this:

<font color = '#FFD441'>This </font>should work<font color = '#584CD5'> just</font> <font color = '#FFB441'>fine</font>.

My solution, after much fiddling, was to add a `<br>` to the previous line and remove the extra blank line in between:

	Write some stuff here.  Then I continue on and want to add some colorful font on a new line:<br>
	<font color = '#FFD441'>This </font>should work<font color = '#584CD5'> just</font> <font color = '#FFB441'>fine</font>.

That worked out okay, but isn't ideal.  Anyone got any insights on this one?