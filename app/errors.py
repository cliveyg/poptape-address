# app/errors.py

from flask import jsonify

# -----------------------------------------------------------------------------
# any custom errors can be put here
# -----------------------------------------------------------------------------

# register global too many requests handler - useful for
# returning json when limit in limiter is reached
def handle_429_request(e):
    return jsonify({ 'message': 'chill out and give it a rest man' }), 429
