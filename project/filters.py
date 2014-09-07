from app import app

import util

app.jinja_env.filters['datetime'] = util.format_date
