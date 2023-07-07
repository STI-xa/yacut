from flask import flash, redirect, render_template

from . import app, db
from .constants import URL_MAX_LENGTH
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)

    short_url = form.custom_id.data
    if URLMap.query.filter_by(short=short_url).first() is not None:
        flash(f'Имя {short_url} уже занято!')
        form.custom_id.data = None
        return render_template('index.html', form=form)
    if short_url is None or short_url == '':
        form.custom_id.data = get_unique_short_id()
    if len(form.custom_id.data) > URL_MAX_LENGTH:
        flash('Указано недопустимое имя для короткой ссылки.')
        form.custom_id.data = None
        return render_template('index.html', form=form)
    url_map = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data,
    )
    db.session.add(url_map)
    db.session.commit()

    return render_template('index.html', form=form, short=url_map)


@app.route('/<string:short>')
def redirection_view(short):
    map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(map.original)
