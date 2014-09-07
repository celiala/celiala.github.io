from flask import render_template
from flask.ext.flatpages import pygments_style_defs

from app import app, pages

import util

posts = util.get_posts()

base = {
    'most_recent': util.get_recent(posts)
}


@app.route('/')
def home():
    page = pages.get_or_404(posts[0].path)
    return render_template('page.html', page=page, base=base, nav='home')


@app.route('/archives/')
def archives():
    return render_template('archives.html', pages=posts, base=base, nav='archives')


@app.route('/blog/<path:path>/')
def page(path):
    # Path is the filename of a page, without the file extension
    # e.g. "first-post"
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, base=base, nav='archives')


@app.route('/tag/<tag_name>/')
def tag(tag_name):
    with_tag = util.filter_by(posts, tag=tag_name)
    return render_template('tag.html', tag=tag_name, pages=with_tag, base=base,
                           nav='archives')


@app.route('/static/css/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}
