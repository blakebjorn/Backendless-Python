## Backendless-Python
Python wrapper for Backendless MBaaS REST API

Dependencies: Requests

This currently only includes very basic functionality (registration, login, updating user fields, logging out). 

Any/all pull requests are welcome.

### Usage

```python
import PyBackendless

APP_ID = "EXAMPLE-ID-E763-ID00-FF7C-AAEFC5DC2100"
REST_KEY = "REST-API-KEY-FFBB-F3C7E118B900"

backendless = PyBackendless.Backendless(APP_ID, REST_KEY)
# Optional parameters + Default values:
  # time_out = 30 # requests connection timeout. Returns {'error':'CONNECTION_TIMEOUT'}
  # verbose = True # prints error exceptions to console

# IMPORTANT: integers/floats in string table objects must be input as such in the payload dictionaries
# json.dumps() does not make this conversion, and backendless will issue a 400 response to non-strings
# If your user identity is the 'name' variable, payload would be {'name':'guy','password':'123456'}
response = backendless.register_user({"email":"example@email.com","password":"123456"}
print response

# The "login" key is mandatory, its value is whatever the 'identity' field of your application is set to
response = backendless.login_user({'login':'example@email.com','password':'123456'})
print response

# Updating a user object 
response = backendless.update_user_object({'name':'guy'})
print response

# Write user-token and info to serialized object
response = backendless.create_token(fileName = "userToken.p")
print response # True or False

# Load user token and re-validate login
del backendless # delete object and reinitialize
backendless = PyBackendless.Backendless(APP_ID, REST_KEY)
response = backendless.read_token("userToken.p")
print response # Same return as initial log-in response
ret = backendless.validate_session() # Check if user-token is still valid
print ret

# if token is still active, renew it with a user-object update
response = backendless.update_user_object({})
print response

# Logging out
response = backendless.logout()
print response
```
