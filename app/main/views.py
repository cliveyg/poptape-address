from app import limiter, db
from flask import jsonify, request, abort
from flask import current_app as app
from app.main import bp
from app.models import Country, Address
from app.decorators import require_access_level

# reject any non-json requests
@bp.before_request
def only_json():
    if not request.is_json:
        abort(400)

# -----------------------------------------------------------------------------
'''
def require_access_level(access_level,request):
    def actual_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            token = request.headers.get('x-access-token')

            if not token:
                return jsonify({ 'message': 'Naughty one!'}), 401

            headers = { 'Content-Type': 'application/json', 'x-access-token': token }
            r = call_requests(app.config['CHECK_ACCESS_URL']+'/login/checkaccess/'+str(access_level), headers)

            if r.status_code != 200:
                return jsonify({ 'message': 'Ooh you are naughty!'}), 401

            returned_json = r.json()

            if 'public_id' in returned_json:
                pub_id = returned_json['public_id']
                return f(pub_id, request, *args, **kwargs)

            return jsonify({ 'message': 'No public_id returned'}), 401

        return decorated
    return actual_decorator
'''
# -----------------------------------------------------------------------------

@bp.route('/address/status', methods=['GET'])
def system_running():
    return jsonify({ 'message': 'System running...' }), 200

# -----------------------------------------------------------------------------

@bp.route('/address/addresses', methods=['GET'])
@require_access_level(10, request)
def get_all_addresses_for_user(public_id, request):

    #addresses = db.session.query().filter(Address.public_id == public_id).all()    

    return jsonify({ 'message': 'returning all addresses' }), 418

# -----------------------------------------------------------------------------

@bp.route('/address/countries', methods=['GET'])
def list_countries():

    countries = []
    results = Country.query.all()

    for country in results:
        country_data = {}
        country_data['name'] = country.name
        country_data['iso_code'] = country.iso_code
        countries.append(country_data)

    return jsonify({ 'countries': countries }), 200

# -----------------------------------------------------------------------------

#@bp.route('/address/<anything_else>', methods=['GET', 'POST', 'PUT', 'DELETE'])
#def return_404():
#    return jsonify({ 'message': 'Nowt \'ere lad' }), 404
