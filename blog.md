---
layout: default
title: Travis Riddle
permalink: /blog/
---

<div class="posts">
  {% for post in site.posts limit: 1 %}
    <article class="post">    
      
      <h1><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h1>

      <div class="entry">
        {{ post.content | truncatewords:50}}
      </div>
      
      <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">Read More</a>
    </article>
  {% endfor %}

  {% for post in site.posts offset:1 %}
  	<li><a href="{{ site.base_url }}{{ post.url }}">{{ post.title }}</a>
  	<span>{{ post.date | date_to_string }}</span></li>
  {% endfor %}
</div>