## Backendless-Python
Python wrapper for Backendless MBaaS REST API

Dependencies: Requests

This currently only includes very basic functionality (registration, login, updating user fields, logging out). 
This is not official in any capacity, nor am I affiliated with Backendless
Any/all pull requests are welcome.

### Usage

```python
import PyBackendless

APP_ID = "EXAMPLE-ID-E763-ID00-FF7C-AAEFC5DC2100"
SECRET_ID = "REST-SECRET-ID-FFBB-F3C7E118B900"

backendless = PyBackendless.Backendless(APP_ID, SECRET_ID)
# Optional parameters + Default values:
  # api_version = "v1" 
  # time_out = 30 # requests connection timeout. Returns {'error':'CONNECTION_TIMEOUT'}
  # verbose = True # prints error exceptions to console

# IMPORTANT: all integers/floats must be input as strings in the payload dictionaries
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
backendless = PyBackendless.Backendless(APP_ID, SECRET_ID)
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
