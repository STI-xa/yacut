import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import LINK_REG, URL_MAX_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

# from urllib.parse import urlparse


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    map = URLMap.query.filter_by(short=short_id).first()
    if map is None:
        raise InvalidAPIUsage('Указанный id не найден',
                              HTTPStatus.NOT_FOUND)
    return jsonify(url=map.original), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        short_id = get_unique_short_id()
    else:
        short_id = data['custom_id']
    if len(short_id) > URL_MAX_LENGTH or not re.match(LINK_REG, short_id):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки',
            HTTPStatus.BAD_REQUEST
        )
    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')

    map = URLMap(original=data['url'], short=short_id)
    db.session.add(map)
    db.session.commit()
    # parsed_url = urlparse(map.original)
    # domain = parsed_url.netloc

    return jsonify(
        short_link='http://localhost/' + map.short, url=map.original), HTTPStatus.CREATED
