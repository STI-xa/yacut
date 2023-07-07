import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(max=256),
                    URL(require_tld=True, message=('Некорректный URL'))]
    )
    custom_id = URLField(
        'Введите свой вариант короткой ссылки',
        validators=[Length(max=16),
                    Optional(),
                    Regexp(re.compile(r'^[a-zA-Z0-9-_]+$'),
                           message='Недопустимые символы')]
    )
    submit = SubmitField('Создать')
