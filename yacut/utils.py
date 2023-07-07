import random
import string

from . import db
from .models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=6))
        if not db.session.query(db.exists().where(URLMap.short == short_id)).scalar():
            return short_id
