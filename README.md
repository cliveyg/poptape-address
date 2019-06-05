# poptape-address
Address microservice in Python Flask

A microservice that stores address data in a postgres database.

###API routes

```
/address [GET] (Authenticated) - Returns a list of addresses for the authenticated user. Possible return codes: [200, 404, 401, 502]
/address [POST] (Authenticated) - Returns a UUID of the address if create is successful. Possible return codes: [200 400 401 422]
/address/<uuid> [DELETE] (Authenticated) - Deletes the address resource defined by the UUID in the URL. Possible return codes: [204, 401]
/address/<uuid> [GET] (Authenticated) - Returns the address resource defined by the UUID in the URL. Possible return codes: [200, 401, 404]
/address/status [GET] (Unauthenticated) - Returns JSON message. Possible return codes: [200, 401, 404, 502]
/address/countries [GET] (Unauthenticated) - Returns the list of ISO-3166 countries. Fields are 'name' and 'iso_code'. Possible return codes: [200]
/address/admin/address [GET] (Authenticated) - Returns a paginated list of addresses. Possible return codes: [200, 401, 404, 500] 
```

####Note:
Editing of an already existing address is not allowed at present. This is a business rule rather than for any technical reason.

####Rate limiting:
In addition most routes will return an HTTP status of 429 if too many requests are made in a certain space of time. The time frame is set on a route by route basis.

####Address fields allowed in post:
* house\_name
* house\_number
* address\_line\_1
* address\_line\_2
* address\_line\_3
* state\_region\_county
* post\_zip\_code
* iso\_code - Three digit ISO-3166 code - checked by JSON schema.

All fields apart from iso\_code are optional but will be eventually validated in more detail by JSON schemas for each individual country. 

####TODO
* Add more admin only routes for bulk actions etc.
* Dockerize the application and run under wsgi.
* Need to add per country json schemas.
* 95% test coverage - Most of the missing parts are due to mocking of authenticating decorator.

