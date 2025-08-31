from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime


class Watchlist(Document):
    name = StringField(required=True, description='The name of the watchlist')
    username = StringField(required=True, description='The username of the watchlist owner')
    movies_id = ListField(StringField())
    updated_date = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'watchlist'
    }