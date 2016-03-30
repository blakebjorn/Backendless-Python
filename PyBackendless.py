# -*- coding: utf-8 -*-
"""
Wrapper for Backendless REST API basic functionality including:
1) Registering user
2) Logging in an existing user
3) Updating user objects
4) Logging out

https://github.com/blakebjorn/Backendless-Python
Pretty much any pull request will be accepted
"""
from __future__ import print_function
import requests
import json


import time

class Backendless():
    def __init__(self, application_id, secret_id, api_version="v1", time_out=30, verbose=True):
        self.applicationId = application_id
        self.secretId = secret_id
        self.apiVersion = api_version
        self.timeOut = time_out #network timeout on requests
        self.baseUrl = "https://api.backendless.com/"+self.apiVersion
        
        self.generalHeaders = {'application-id': self.applicationId,
                                'secret-key': self.secretId,
                                'Content-type':'application/json',
                                'application-type': 'REST'}
                                
        self.activeLogin = False
        self.verbose = verbose
        
    def initialize_user(self, response):
        self.objectId = response.json().pop('objectId')
        self.userToken = response.json().pop('user-token')
        self.userData = response.json()
        self.userHeaders = dict(self.generalHeaders)
        self.userHeaders['user-token'] = self.userToken
        self.activeLogin = True
        
    def post_request(self, url, headers, data):
        try:
            response = requests.post(url, data=data, headers=headers, timeout=self.timeOut)
        except Exception as e:
            if self.verbose:
                print(e)
            response = self.handle_response(e)               
        return response

    def put_request(self, url, headers, data):
        try:
            response = requests.put(url, data=data, headers=headers, timeout=self.timeOut)
        except Exception as e:
            if self.verbose:
                print(e)
            response = self.handle_response(e)
        return response

    def get_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=self.timeOut)
        except Exception as e:
            if self.verbose:
                print(e)
            response = self.handle_response(e)  
        return response
    
    def handle_response(self, e):
        if e==requests.exceptions.Timeout:
            response = {'error':'CONNECTION_TIMEOUT'}
        elif e==requests.exceptions.ConnectionError:
            response = {'error':'CONNECTION_ERROR'}
        elif e==requests.exceptions.HTTPError:
            response = {'error':'HTTP_ERROR'}
        elif e== requests.exceptions.TooManyRedirects:
            response = {'error':'TOO_MANY_REDIRECTS_ERROR'}
        elif e== requests.exceptions.RequestException:
            response = {'error':'UNSPECIFIED_REQUEST_ERROR'}
        elif e== simplejson.scanner.JSONDecodeError:
            response = {'error':'JSON_DECODING_ERROR'}
        else:
            response = {'error':'UNKNOWN_ERROR'}
        
    def register_user(self, data):
        """
        Creates new user object.

        :param data: dictionary with format {"email":"XXX@YYY.ZZZ","password":"foo"}, where "email" is the "identity" entry
        :type data: dict

        :return: Json response
        :rtype : dict
        """
        requestUrl = self.baseUrl+"/data/Users"
        headers = self.generalHeaders
        response = self.post_request(requestUrl, headers, json.dumps(data))
        if type(response)==requests.models.Response:
            response = response.json()
        return response
    
    def login_user(self, data):
        """
        Logs in to an existing user. Saves user ID, login token, and user data to the variables: objectId, userToken, and userData, respectively.

        :param data: dictionary with format {"login":"XXX@YYY.ZZZ","password":"foo"}. The "login" value is the user "identity" entry
        :type data: dict

        :return: Json response
        :rtype : dict
        """
        if not self.activeLogin:
            requestUrl = self.baseUrl+"/users/login"
            headers = self.generalHeaders
            response = self.post_request(requestUrl, headers, json.dumps(data))
            if response.status_code==200:
                self.initialize_user(response)
            if type(response)==requests.models.Response:
                response = response.json()
            return response
        else:
            return {'error':'Must log out before logging in again'}
    
    def update_user_object(self,data):
        """
        Updates a field for the logged in user.
        
        :param data: dictionary with format {"field":"value","field2":"value2"}
        :type data: dict

        :return: Json response
        :rtype : dict
        """
        if self.activeLogin:
            headers = self.userHeaders
            requestUrl = self.baseUrl+"/users/"+str(self.objectId)
            response = self.put_request(requestUrl, headers, json.dumps(data))
            if type(response)==requests.models.Response:
                response = response.json()
            return response
        else:
            return {'error':"Must log in before updating user objects"}
            
    def logout(self):
        """
        Logs out the active user.
        
        :return: Json response
        :rtype : dict
        """
        if self.activeLogin:
            requestUrl = self.baseUrl+"/users/logout"
            headers = dict(self.userHeaders)
            headers.pop("Content-type")
            response = self.get_request(requestUrl, headers)
            if response.status_code==200:
                self.activeLogin=False
                response={'message':'Logout Successful'}
            if type(response)==requests.models.Response:
                response = response.json()
            return response
        else:
            return {'error':"Must log in before logging out users"}
