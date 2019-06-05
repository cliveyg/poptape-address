# app/tests/test_api.py
from mock import patch
from .fixtures import addCountries, addAddresses, getPublicID
from functools import wraps
from flask import jsonify

# have to mock the require_access_level decorator here before it 
# gets attached to any classes or functions
def mock_dec(access_level,request):
    def actual_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            token = request.headers.get('x-access-token')

            if not token:
                return jsonify({ 'message': 'Naughty one!'}), 401
            pub_id = getPublicID()
            return f(pub_id, request, *args, **kwargs)

        return decorated
    return actual_decorator

patch('app.decorators.require_access_level', mock_dec).start()

from app import create_app, db
from app.models import Country, Address
from app.config import TestConfig

from flask import current_app 
from flask_testing import TestCase as FlaskTestCase

from sqlalchemy.exc import DataError

###############################################################################
####                      flask test case instance                         ####
###############################################################################

class MyTest(FlaskTestCase):

    ############################
    #### setup and teardown ####
    ############################

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

###############################################################################
####                               tests                                   ####
###############################################################################

    def test_for_testdb(self):
        self.assertTrue('poptape_address_test' in 
                        self.app.config['SQLALCHEMY_DATABASE_URI'])

# -----------------------------------------------------------------------------

    def test_status_ok(self):
        headers = { 'Content-type': 'application/json' }
        response = self.client.get('/address/status', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

# -----------------------------------------------------------------------------

    def test_404(self):
        # this behaviour is slightly different to live as we've mocked the 
        headers = { 'Content-type': 'application/json' }
        response = self.client.get('/address/resourcenotfound', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 404)

# -----------------------------------------------------------------------------

    def test_api_rejects_html_input(self):
        headers = { 'Content-type': 'text/html' }
        response = self.client.get('/address/status', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

# -----------------------------------------------------------------------------

    def test_country_model_saves_ok(self):
        country = Country(name = "United Kingdom",
                          iso_code = "GBR")
        db.session.add(country)
        db.session.commit()
        self.assertEqual(country.id, 1)

# -----------------------------------------------------------------------------

    def test_country_model_fails_iso_length(self):
        country = Country(name = "United Kingdom",
                          iso_code = "TOOLONG")
        try:
            db.session.add(country)
            db.session.commit()
        except DataError as error:
            db.session.rollback()
            self.assertTrue('value too long' in str(error))

# -----------------------------------------------------------------------------

    def test_return_list_of_countries(self):
        countries = addCountries() 
        headers = { 'Content-type': 'application/json' }
        response = self.client.get('/address/countries', headers=headers, follow_redirects=True)
        results = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results.get('countries')), 4)

# -----------------------------------------------------------------------------

    def test_api_rejects_unauthenticated_get(self):
        headers = { 'Content-type': 'application/json' }
        response = self.client.get('/address', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 401)

# -----------------------------------------------------------------------------

    def test_list_of_addresses_ok(self):
        addresses = addAddresses()
        headers = { 'Content-type': 'application/json', 'x-access-token': 'somefaketoken' }
        response = self.client.get('/address', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # expect the number of returned addresses to be 3 as we are filtering by public_id
        results = response.json
        self.assertEqual(len(results.get('addresses')), 3)
        # get the retuned address with country name of Brazil and check the returned data matches
        original_brazil_address = None
        for addy in addresses:
            if addy.country_id == 3:
                original_brazil_address = addy

        returned_brazil_address = None
        for returned_addy in results['addresses']:
            if returned_addy.get('country') == "Brazil":
                returned_brazil_address = returned_addy

        self.assertEqual(original_brazil_address.post_zip_code, returned_brazil_address.get('post_zip_code'))

# -----------------------------------------------------------------------------

    def test_all_addresses_admin_incl_paging(self):
        addresses = addAddresses()
        headers = { 'Content-type': 'application/json', 'x-access-token': 'somefaketoken' }
        response = self.client.get('/address/admin/address', headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        results = response.json
        # test total number of records and limit per page equals config
        add_limit_per_page = int(TestConfig.ADDRESS_LIMIT_PER_PAGE)
        self.assertEqual(len(results.get('addresses')), add_limit_per_page)
        self.assertEqual(results.get('total_records'), 6)

# -----------------------------------------------------------------------------

