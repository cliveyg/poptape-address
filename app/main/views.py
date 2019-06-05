# app/main/views.py
from app import limiter, db, flask_uuid
from flask import jsonify, request, abort, url_for
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
# helper route - useful for checking status of api in api_server application

@bp.route('/address/status', methods=['GET'])
@limiter.limit("100/hour")
def system_running():
    return jsonify({ 'message': 'System running...' }), 200

# -----------------------------------------------------------------------------
# returns a list of addresses for the authenticated user

@bp.route('/address', methods=['GET'])
@limiter.limit("20/hour")
@require_access_level(10, request)
def get_all_addresses_for_user(public_id, request):

    addresses = []
    try:
        addresses = db.session.query(Address.address_id,
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
# creates an address for the authenticated user

@bp.route('/address', methods=['POST'])
@limiter.limit("10/hour")
@require_access_level(10, request)
def get_create_address_for_user(public_id, request):

    return jsonify({ 'message': 'dunno what you expected but yer not getting it' }), 417

# -----------------------------------------------------------------------------
# returns an individual address - returns 401 if not authorized on that
# address uuid

@bp.route('/address/<uuid:address_id>', methods=['GET'])
@limiter.limit("100/hour")
@require_access_level(10, request)
def get_one_address(public_id, request, address_id):

    # convert to string
    address_id = str(address_id)
    address = None
    try:
        address = db.session.query(Address.house_name,
                                   Address.house_number,
                                   Address.address_line_1,
                                   Address.address_line_2,
                                   Address.address_line_3,
                                   Address.state_region_county,
                                   Country.name,
                                   Country.iso_code,
                                   Address.post_zip_code).join(Country).filter(Address.address_id == address_id).first()
    except:
        return jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 502

    if not address:
        message = "no addresses found for supplied id ["+address_id+"]"
        return jsonify({ 'message': message }), 404

    # i prefer to explicitly assign variables returned to ensure no 
    # accidental exposure of private data
    address_data = {}
    address_data['house_name'] = address.house_name
    address_data['house_number'] = address.house_number
    address_data['address_line_1'] = address.address_line_1
    address_data['address_line_2'] = address.address_line_2
    address_data['address_line_3'] = address.address_line_3
    address_data['state_region_county'] = address.state_region_county
    address_data['country'] = address.name
    address_data['country_code'] = address.iso_code
    address_data['post_zip_code'] = address.post_zip_code

    return jsonify(address_data), 200

# -----------------------------------------------------------------------------
# deletes an address for the authenticated user

@bp.route('/address/<uuid:address_id>', methods=['DELETE'])
@require_access_level(10, request)
def delete_address_for_user(public_id, request, address_id):

    return jsonify({ 'message': 'dunno what you expected but yer not getting it' }), 417

# -----------------------------------------------------------------------------
# returns a list of all possible countries - names and 3 alpha iso codes

@bp.route('/address/countries', methods=['GET'])
@limiter.limit("100/hour")
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
# admin routes
# -----------------------------------------------------------------------------


@bp.route('/address/admin/address', methods=['GET'])
@limiter.limit("100/hour")
@require_access_level(5, request)
def get_all_addresses_admin_method(public_id, request):

    # pagination allowed on this url
    page = request.args.get('page', 1, type=int)

    addresses = []
    total_records = 0
    addresses_per_page = int(app.config['ADDRESS_LIMIT_PER_PAGE'])
    try:
        total_records = db.session.query(Address).count() 

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
                                     Address.post_zip_code).join(Country).paginate(page, addresses_per_page, False).items

    except:
        return jsonify({ 'message': 'oopsy, sorry we couldn\'t complete your request' }), 500

    if len(addresses) == 0:
        return jsonify({ 'message': 'no addresses found for user' }), 404

    adds = []
    for address in addresses:
        address_data = {}
        address_data['address_id'] = address.address_id
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

    output = { 'addresses': adds }
    output['total_records'] = total_records
    total_so_far = page * addresses_per_page
    
    if total_so_far < total_records:
        npage = page + 1
        output['next_url'] = '/address/admin/address?page='+str(npage)

    if page > 1:
        ppage = page - 1
        output['prev_url'] = '/address/admin/address?page='+str(ppage)

    return jsonify(output), 200

# -----------------------------------------------------------------------------
# route for testing rate limit works - generates 429 if more than two calls
# per minute to this route - restricted to admin users and above
@bp.route('/address/admin/ratelimited', methods=['GET'])
@require_access_level(5, request)
@limiter.limit("2/minute")
def rate_limted(public_id, request):
    return jsonify({ 'message': 'first time good' }), 200

# -----------------------------------------------------------------------------
# route for anything left over - generates 404

@bp.route('/address/<everything_left>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def not_found(everything_left):
    message = 'resource ['+everything_left+'] not found'
    return jsonify({ 'message': message }), 404
