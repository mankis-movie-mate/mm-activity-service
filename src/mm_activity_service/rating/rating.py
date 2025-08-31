from mongoengine import Document, IntField, StringField, ListField, DateTimeField
from datetime import datetime


class Rating(Document):
    username = StringField(required=True)
    movie_id = StringField(required=True)
    rate = IntField(required=True)
    review_text = StringField()
    tags = ListField(StringField())
    timestamp = DateTimeField(default=datetime.now)
    update_date = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'ratings'
    }