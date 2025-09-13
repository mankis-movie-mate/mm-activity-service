import logging
from datetime import datetime
from mm_activity_service.utils import data_response, message_response
from mm_activity_service.watchlist.watchlist import Watchlist
from flask_restx import Namespace, Resource, fields
from flask import Response, request
import json
from mm_activity_service.events.publisher import get_publisher
from mm_activity_service.config.config import Config
from mm_activity_service.events.models import ActivityEvent, Action

ns = Namespace('watchlist', description='Watchlist related operations')
logger = logging.getLogger(__name__)
publisher = get_publisher(Config())

watchlist_dto = ns.model('Watchlist', {
    'name': fields.String(required=True, description='The name of the watchlist'),
    'username': fields.String(required=True, description='The username of the watchlist owner'),
    'movies_id': fields.List(fields.String, description='List of movie IDs in the watchlist')
})

@ns.route('/')
class WatchlistCreateResource(Resource):
    @ns.expect(watchlist_dto)
    def post(self) -> Response:
        data = ns.payload
        name = data.get('name')
        username = data.get('username')
        movies_id = data.get('movies_id', [])
        if not name or not username:
            logger.warning("Missing required fields for watchlist creation")
            return message_response("Missing required fields for watchlist creation", 400)
        logger.info(f"Creating watchlist '{name}' for user '{username}' with movies {movies_id}")

        if Watchlist.objects(name=name, username=username).first():
            return message_response(f"Watchlist '{name}' already exists for user '{username}'", 400)

        watchlist = Watchlist(name=name, username=username, movies_id=movies_id)
        watchlist.save()
        return data_response(watchlist.to_json())


@ns.route('/all-by-user/<string:username>')
class WatchlistAllByUserResource(Resource):
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('size', 'Number of items per page', type=int, default=10)
    def get(self, username: str) -> Response:
        try:
            page_number = max(1, int(request.args.get('page', 1)))
            page_size = max(1, int(request.args.get('size', 10)))
        except ValueError:
            return message_response("Invalid page number", 400)

        logger.info(f'Getting watchlists for user {username}, page {page_number}, page_size {page_size}')
        total_count = Watchlist.objects(username=username).count()
        total_pages = (total_count + page_size - 1) // page_size if page_size else 1

        if total_count == 0:
            return message_response(f"No watchlists found for user {username}", 404)

        if page_number > total_pages:
            return message_response(f"Page number {page_number} exceeds total pages {total_pages}", 400)

        watchlists = Watchlist.objects(username=username).skip((page_number - 1) * page_size).limit(page_size)
        response_data = {
            'elements': json.loads(watchlists.to_json()),
            'pageNo': page_number,
            'pageSize': page_size,
            'totalElements': total_count,
            'totalPages': total_pages,
            'isLast': page_number >= total_pages
        }
        return data_response(json.dumps(response_data))


@ns.route('/<string:watchlist_id>')
class WatchlistByIdResource(Resource):
    def get(self, watchlist_id: str) -> Response:
        logger.info(f'Getting watchlist with ID {watchlist_id}')
        watchlist = Watchlist.objects(id=watchlist_id).first()
        if watchlist:
            return data_response(watchlist.to_json())
        else:
            return message_response(f"Watchlist with ID {watchlist} not found", 404)

    @ns.expect(watchlist_dto)
    def patch(self, watchlist_id: str) -> Response:
        data = ns.payload
        name = data.get('name')
        username = data.get('username')
        movies_id = data.get('movies_id', [])
        logger.info(f"Updating watchlist ID {watchlist_id} with name '{name}' and movies {movies_id}")

        watchlist = Watchlist.objects(id=watchlist_id).first()
        if watchlist:
            watchlist.name = name
            watchlist.movies_id = movies_id
            watchlist.updated_date = datetime.now()
            watchlist.save()
            if movies_id:
                for movie_id in movies_id:
                    event = ActivityEvent(
                        userId=username,
                        movieId=movie_id,
                        action=Action.WATCHLISTED,
                        timestamp=int(datetime.now().timestamp() * 1000)
                    )
                    publisher.publish(event)
                    return data_response(watchlist.to_json())
        else:
            return message_response(f"Watchlist with ID {watchlist_id} not found", 404)

    def delete(self, watchlist_id: str) -> Response:
        logger.info(f"Deleting watchlist with ID {watchlist_id}")

        watchlist = Watchlist.objects(id=watchlist_id).first()
        if watchlist:
            watchlist.delete()
            return message_response(f"Watchlist with ID {watchlist_id} deleted", 200)
        else:
            return message_response(f"Watchlist with ID {watchlist_id} not found", 404)