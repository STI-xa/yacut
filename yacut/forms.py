from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256),
                    URL(require_tld=True, message=('Некорректный URL'))]
    )
    custom_id = URLField(
        'Введите свой вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
