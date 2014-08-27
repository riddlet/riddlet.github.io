---
layout: post
title: Test
---

Test for completeness.

This is an image of an iris
![Flower](http://wiki.irises.org/pub/TbKthruO/TbMillenniumFalcon/Millenium_Falcon2_2005May.jpg)

And so is this:
![Eye](http://upload.wikimedia.org/wikipedia/commons/4/41/Menschliches_Auge.jpg)

This is a [link](http://www.columbia.edu/cu/psychology/vpvaughns/index.html)

A big header
==============

A smaller header
-----------------

# Atx head 1

## Atx head 2 ##

### Atx head 3 ###

Back to plain text.  Some riddles:


#### Riddle 1
>Voiceless it cries,
>Wingless flutters
>toothless bites
>Mouthless mutters

#### Riddle 2
>Alive without breath,
>As cold as death;
>Never thirsy, ever drinking,
>All in mail never clinking

#### Spoilers
1. Wind
2. Fish

What about code?  Here's how I get a list excel files from the directory where the raw writing data is stored:

	files=glob.glob("/Users/triddle/Documents/XmlGitTest/*/*.xls*")

Then using that, I get  some data and assign a variable:

	coh1 = pd.read_excel(files[0], 'Sheet1') #get data from excel file
	coh1['Grade Level'] = 8 #assign new variable for grade level

This is a horizontal rule

* * *

And so is this

*****

And this

--------------------

Table:

Let's generate a table:

<table>
	<tr>
		<td>A</td>
		<td>B</td>
		<td>C</td>
	</tr>
	<tr>
		<td>1</td>
		<td>2</td>
		<td>3</td>
	</tr>
</table>

Finally, sometimes we wish to add *emphasis*.  And every once in a while **extra emphasis**

