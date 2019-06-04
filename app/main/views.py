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

@bp.route('/address/status', methods=['GET'])
def system_running():
    return jsonify({ 'message': 'System running...' }), 200

# -----------------------------------------------------------------------------

@bp.route('/address/addresses', methods=['GET'])
@require_access_level(10, request)
def get_all_addresses_for_user(public_id, request):

    addresses = []
    try:
        addresses = db.session.query(Address.address_id,
                                     Address.public_id,
                                     Address.house_name,
                                     Address.house_number,
                                     Address.address_line_1,
                                     Address.address_line_2,
                                     Address.address_line_3,
                                     Address.state_region_county,
                                     Country.name,
                                     Country.iso_code,
                                     Address.post_zip_code).join(Country).filter(Address.public_id == public_id).all()

    except: 
        jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 502

    if len(addresses) == 0:
        return jsonify({ 'message': 'no addresses found for user' }), 404

    adds = []
    for address in addresses:
        address_data = {}
        address_data['address_id'] = address.address_id
        address_data['public_id'] = address.public_id
        address_data['house_name'] = address.house_name
        address_data['house_number'] = address.house_number
        address_data['address_line_1'] = address.address_line_1
        address_data['address_line_2'] = address.address_line_2
        address_data['address_line_3'] = address.address_line_3
        address_data['state_region_county'] = address.state_region_county
        address_data['country'] = address.name
        address_data['country_code'] = address.iso_code
        address_data['post_zip_code'] = address.post_zip_code
        adds.append(address_data)

    return jsonify({ 'addresses': adds }), 200

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
