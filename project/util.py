import arrow

from app import pages


def get_posts():
    posts = [page for page in pages if 'date' in page.meta]
    return sorted(posts, reverse=True, key=lambda page: arrow.get(page.meta['date']))


def filter_by(posts, tag):
    return [post for post in posts if ('tags' in post.meta and tag in post.meta['tags'].split())]


def get_recent(posts):
    return posts[:5]


def format_date(value):
    return arrow.get(value).format("MMM D, YYYY")
