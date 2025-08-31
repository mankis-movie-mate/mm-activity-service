import logging
from datetime import datetime

from mm_activity_service.utils import data_response, message_response
from mm_activity_service.rating.rating import Rating
from flask_restx import Namespace, Resource, fields
from flask import Response, request
import json

ns = Namespace('rating', description='Rating related operations')
logger = logging.getLogger(__name__)

rating_dto = ns.model('Rating', {
    'movie_id': fields.String(required=True, description='The ID of the movie being rated'),
    'username': fields.String(required=True, description='The username of the rater'),
    'rate': fields.Integer(required=True, description='The rating value (1-5)', min=1, max=5),
    'review': fields.String(description='Optional review text'),
    'tags': fields.List(fields.String, description='Optional list of tags associated with the rating')
})


@ns.route('/')
class RatingResource(Resource):
    @ns.expect(rating_dto)
    def post(self) -> Response:
        data = ns.payload
        rate = data.get('rate')
        movie_id = data.get('movie_id')
        username = data.get('username')
        review = data.get('review', '')
        tags = data.get('tags', [])

        if not rate or not movie_id or not username:
            logger.info("Missing required fields for rating creation")
            return message_response("Missing required fields for rating creation", 400)

        if not (1 <= rate <= 5):
            logger.info("Rating value must be between 1 and 5")
            return message_response("Rating value must be between 1 and 5", 400)

        logger.info(f"Creating rating for movie '{movie_id}' by user '{username}' with rate {rate}, review '{review}', and tags {tags}")
        rating = Rating(username=username, movie_id=movie_id, rate=rate, review_text=review, tags=tags, timestamp=datetime.now(), update_date=datetime.now())
        rating.save()
        return data_response(rating.to_json(), 201)


@ns.route('/movie/<string:movie_id>')
class RatingByMovieIdResource(Resource):
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('size', 'Number of items per page', type=int, default=10)
    def get(self, movie_id: str) -> Response:
        try:
            page_number = max(1, int(request.args.get('page', 1)))
            page_size = max(1, int(request.args.get('size', 10)))
        except ValueError:
            return message_response("Invalid page number", 400)

        logger.info(f'Getting ratings for movie {movie_id}, page {page_number}, page_size {page_size}')
        total_count = Rating.objects(movie_id=movie_id).count()
        total_pages = (total_count + page_size - 1) // page_size if page_size else 1

        if total_count == 0:
            return message_response(f"No ratings found for movie {movie_id}", 404)

        if page_number > total_pages:
            return message_response(f"Page number {page_number} exceeds total pages {total_pages}", 400)

        ratings = Rating.objects(movie_id=movie_id).skip((page_number - 1) * page_size).limit(page_size)
        response_data = {
            'elements': json.loads(ratings.to_json()),
            'pageNo': page_number,
            'pageSize': page_size,
            'totalElements': total_count,
            'totalPages': total_pages,
            'isLast': page_number >= total_pages
        }
        return data_response(json.dumps(response_data))


@ns.route('/<string:rating_id>')
class RatingByIdResource(Resource):
    def get(self, rating_id: str) -> Response:
        logger.info(f'Getting rating with ID {rating_id}')
        rating = Rating.objects(id=rating_id).first()
        if rating:
            return data_response(rating.to_json())

        return message_response(f"Rating with ID {rating_id} not found", 404)

    @ns.expect(rating_dto)
    def patch(self, rating_id: str) -> Response:
        data = ns.payload
        rate = data.get('rate')
        review = data.get('review', '')
        tags = data.get('tags', [])

        logger.info(f'Updating rating with ID {rating_id}')
        rating = Rating.objects(id=rating_id).first()
        if not rating:
            return message_response(f"Rating with ID {rating_id} not found", 404)

        if rate:
            if not (1 <= rate <= 5):
                logger.info("Rating value must be an integer between 1 and 5")
                return message_response("Rating value must be an integer between 1 and 5", 400)
            rating.rate = rate

        rating.review_text = review
        rating.tags = tags
        rating.save()
        return data_response(rating.to_json())

    def delete(self, rating_id: str) -> Response:
        logger.info(f'Deleting rating with ID {rating_id}')
        rating = Rating.objects(id=rating_id).first()
        if rating:
            rating.delete()
            return message_response(f"Rating with ID {rating_id} deleted successfully", 200)

        return message_response(f"Rating with ID {rating_id} not found", 404)