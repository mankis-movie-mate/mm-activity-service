import json
from flask import Response


def data_response(data, status=200) -> Response:
    return Response(data, status=status, mimetype='application/json')


def message_response(message: str, status) -> Response:
    return Response(json.dumps({'message': message}), status=status, mimetype='application/json')