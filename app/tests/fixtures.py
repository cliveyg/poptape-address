# app/tests/fixtures.py
from app import db
from app.models import Country, Address

# countries and addresses for testings

def getPublicID():
    return "fef0b81e-6b39-417c-ab4f-4be1ac4f2c66"

def addCountries():
    country1 = Country(name = "United Kingdom", iso_code = "GBR")
    country2 = Country(name= "Germany", iso_code = "DEU")
    country3 = Country(name= "Brazil", iso_code = "BRA")
    country4 = Country(name= "France", iso_code = "FRA")
    db.session.add(country1)
    db.session.add(country2)
    db.session.add(country3)
    db.session.add(country4)
    countries = [country1, country2, country3, country4]
    db.session.commit()
    return countries

def addAddresses():
    pass
