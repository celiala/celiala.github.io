title: Making a blog on GitHub using Flask
date: 2014-09-07
tags: python flask

## Finding a starter template

I've been wanting a blog for a while. I could have used WordPress but I really wanted to make my 
own learning and using Flask and Bootstrap. In addition:

- I wanted it to be easy to write up new blog posts. I didn't want to deal with writing lots of HTML markup.
- I didn't want to spend lots of money on web hosting
- I wanted to show code snippets

I ended up using example from Steven Loria 
using [Flask-FlatPages, Frozen-Flask, 
and Github Pages](http://stevenloria.com/hosting-static-flask-sites-for-free-on-github-pages/). This
solution is great because Github Pages are free, and Flask-FlatPages allows you to write your entries
in markdown (almost text-like). Markdown also allows for showing code snippets, although by default
the code is not highlighted.

The code for this site is up at: [https://github.com/celiala/celiala.github.io](https://github.com/celiala/celiala.github.io)

## Adding more features

The above solution gave me a list of all posts and a template for each post. But I didn't want my
default page to a list of all my posts. Instead I wanted my homepage to display my most recent
entry. I also wanted:
 
- the ability to tag my posts
- a site using Twitter Bootstrap
- a side nav showing just the most recent posts (eg: the last 5)

### Adding tags to posts

The format for a Flask-FlatPages entry is: metadata mapping, a blank line, then the page body in
markdown. The default example `project/pages/hello.md` shows a title, date, and the blog body:

    title: Hello
    date: 2010-12-22
    
    Hello, *World*!
    
    Lorem ipsum dolor sit amet, ...


Turns out that adding tags to FlatPages is super simple - simply add it as metadata:

    title: Hello
    date: 2010-12-22
    tags: python flask
    
    Hello, *World*!

Then in `project/views.py` you can create view for all entries for that tag:

    from app import pages
    
    @app.route('/tag/<tag_name>/')
    def tag(tag_name):
        with_tag = [post for post in pages if 'tags' in post.meta and tag_name in post.meta['tags'].split() ]
        return render_template('tag.html', tag=tag_name, pages=with_tag)
    
## Integrating Twitter Bootstrap

The next step was to integrate Twitter Bootstrap. This was pretty easy, since they have a lot
of [great starter examples](http://getbootstrap.com/getting-started/#examples). 
I ended up using their [blog template](http://getbootstrap.com/examples/blog/).

## Making the homepage my most recent entry

In order to get my homepage the most recent entry, I simply got all the entries, sorted them
in descending chronological order, then fed that path to the FlatPages HTML renderer (the `pages.get_or_404` method)

    @app.route('/')
    def home():
        posts = [page for page in pages if 'date' in page.meta]
        sorted_posts = sorted(posts, reverse=True, key=lambda page: page.meta['date'])
        page = pages.get_or_404(sorted_posts[0].path)
        return render_template('page.html', page=page)

## Code highlighting code snippets

*[Note that this isn't 100% to my liking but it's a good start, see conclusion notes]*

To get code highlighting, simply use `pygments_style_defs` to dynamically render the css formatting, 
then refer to it from your template.

In `projects/views.py`:

    from flask.ext.flatpages import pygments_style_defs

    ...
    
    @app.route('/pygments.css')
    def pygments_css():
        return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}

Then in `projects/base.html`:

    <link rel="stylesheet" href="{{ url_for('pygments_css') }}">

## Conclusion

There are still a few things that I want to add/fix, but this is good-enough to get me up-and-running. Here are
some things I want to do for iteration #2:

- The code formatting looks wonky for Python; I'd like to fix that
- I want to add 'Prev' and 'Next' links to blog entries
- It would be great to have a summary outline above each post (eg extract/format all the headers) 
- Including the timestamp in the filename will probably help with organization in the future. In 
that case, it would be great to pull the timestamp directly from the path instead.

I hope this is helpful to others. If there's something missing, feel free to let me know. The code 
for all of this is up on github: [https://github.com/celiala/celiala.github.io](https://github.com/celiala/celiala.github.io)

