from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime


class Watchlist(Document):
    name = StringField(required=True)
    username = StringField(required=True)
    movies_id = ListField(StringField())
    updated_date = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'watchlist'
    }