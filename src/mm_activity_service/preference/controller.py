import logging
from mm_activity_service.utils import data_response, message_response
from mm_activity_service.preference.preference import UserPreference
from flask_restx import Namespace, Resource, fields
from flask import Response

ns = Namespace('preferences', description='User Preferences operations')
logger = logging.getLogger(__name__)


preference_dto = ns.model('UserPreference', {
    'username': fields.String(required=True, description='The username'),
    'genres_id': fields.List(fields.String, description='List of genre IDs')
})


@ns.route('/<string:username>')
class PreferenceByUsernameResource(Resource):
    def get(self, username: str) -> Response:
        logger.info(f'Getting user preferences for {username}')
        preferences = UserPreference.objects(username=username).first()
        if preferences:
            return data_response(preferences.to_json())

        return message_response(f"Username {username} not found", 404)


@ns.route('/')
class PreferenceResource(Resource):
    @ns.expect(preference_dto)
    def post(self) -> Response:
        data = ns.payload
        username = data.get('username')
        genres_id = data.get('genres_id')
        logger.info(f"Saving user preferences for {username} with genres {genres_id}")

        if not username:
            return message_response("Username is required", 400)

        if UserPreference.objects(username=username).first():
            return message_response(f"Preferences for this username {username} already exist", 400)

        user_pref = UserPreference(username=username, genres_id=genres_id)
        user_pref.save()
        return data_response(user_pref.to_json(), 201)

    @ns.expect(preference_dto)
    def patch(self) -> Response:
        data = ns.payload
        username = data.get('username')
        genres_id = data.get('genres_id')
        logger.info(f"Updating user preferences for {username} with genres {genres_id}")

        user_pref = UserPreference.objects(username=username).first()
        if user_pref:
            user_pref.genres_id = genres_id
            user_pref.save()
            return data_response(user_pref.to_json())

        return message_response(f"Username {username} not found", 404)