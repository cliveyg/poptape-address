# app/decorators.py
import app.services
from functools import wraps
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()

# -----------------------------------------------------------------------------
# this is separate from the views so we can mock it in tests
# -----------------------------------------------------------------------------

def require_access_level(access_level,request):
    def actual_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            token = request.headers.get('x-access-token')

            if not token:
                return jsonify({ 'message': 'Naughty one!'}), 401

            headers = { 'Content-Type': 'application/json', 'x-access-token': token }
            r = app.services.call_requests(os.getenv('CHECK_ACCESS_URL')+'/login/checkaccess/'+str(access_level), headers)

            if r.status_code != 200:
                return jsonify({ 'message': 'Ooh you are naughty!'}), 401

            returned_json = r.json()

            if 'public_id' in returned_json:
                pub_id = returned_json['public_id']
                return f(pub_id, request, *args, **kwargs)

            return jsonify({ 'message': 'No public_id returned'}), 401

        return decorated
    return actual_decorator 
