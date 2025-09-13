

from flask import jsonify

def invalid_request_responce():
    return jsonify({'message': 'Invalid request'}), 400