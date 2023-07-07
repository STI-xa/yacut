import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .constants import REGEXP_VALIDATION


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
                    Regexp(re.compile(REGEXP_VALIDATION),
                           message='Недопустимые символы')]
    )
    submit = SubmitField('Создать')
