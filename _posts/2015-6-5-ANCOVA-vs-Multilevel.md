---
layout: post
title: ANCOVA vs multilevel model
---

I've spent a lot of time recently comparing two methods of analyzing the same dataset.

The data consist of grades in college spanning an entire college career for a number of individuals. These individuals were part of an experiment which one can imagine as being composed of six experimental cells (i.e. a 2x3 design). We'll call the first variable 'group', which has two levels (A and B) and the second 'condition'. The condition variable has three levels (Control, TreatX and TreatY).

Individuals received the intervention at the same calendar time point, but were at different stages in their academic careers (i.e. Freshman, Sophomore, etc.). In looking for an effect of the treatment, my first approach was to fit a series of multilevel models. After going through a model-selection process, I retained a model with a random effect of time and a random intercept, both varying by subject. For the fixed effects, I modeled a main effect of time and a three-way interaction between group, condition, and pre vs. post intervention. The raw data can be seen in Figure 1.

![Grade inflation!](/images/2015_6_5/GPA.jpeg)

**Figure 1: Longitudinal GPA by group and treatment condition. Red bar indicates time of treatment.**

As is probably apparent from the plot, the model suggested no effect of treatment.

Unbeknownst to me, prior to my examining these data, another analyst looked at these data with an ANCOVA approach. Here, we model the GPA in the academic term in which the intervention took place, controlling for GPA in the previous term. Figure 2 displays these data, which are <s>essentially the same as</s> identical to those seen in Figure 1, but we're limiting our view to just two semesters.

![Magical appearing treatment effect](/images/2015_6_5/ANCOVA.jpeg)

**Figure 2: Gpa in the academic term of treatment and in the term prior to treatment as a function of group and condition.**

As you might guess, this one *does* suggest that there's a treatment effect! Here, Group B is receiving a boost from Treatment X. I think this is an example of what Simmons, Nelson, & Simonsohn would refer to as [researcher degrees of freedom](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1850704) - we've got too much flexibility with regards to exploring these data.

There are two interpretations here. The first is that there's no effect of the treatment and the ANCOVA analysis is just a spurious result. The second is that there is an effect of the treatment, but it's transitive, disappating over time. All I've shown is raw data. Which is more believable to you?