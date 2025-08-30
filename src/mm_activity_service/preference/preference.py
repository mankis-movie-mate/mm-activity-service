from mongoengine import Document, StringField, ListField


class UserPreference(Document):
    username = StringField(required=True)
    genres_id = ListField(StringField())

    meta = {
        'collection': 'user_preferences'
    }