import random
import string

from . import db
from .models import URLMap
from .constants import SHORT_URL_MAX_LENGTH


def get_unique_short_id():
    while True:
        short_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=SHORT_URL_MAX_LENGTH))
        if not db.session.query(db.exists().where(URLMap.short == short_id)).scalar():
            return short_id
