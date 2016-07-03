#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

import sys
if (sys.version_info > (3, 0)):
    import http.client
else:
    import requests
import urllib
import json
import hashlib
import time

HTTPS_VERIFY = True
TIMEOUT      = 10

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()

if (sys.version_info > (3, 0)):
    def httpGet(url,resource,params=''):
        conn = http.client.HTTPSConnection(url, timeout=10)
        conn.request("GET",resource + '?' + params)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        return json.loads(data)

    def httpPost(url,resource,params):
         headers = {
                "Content-type" : "application/x-www-form-urlencoded",
         }
         conn = http.client.HTTPSConnection(url, timeout=10)
         temp_params = urllib.parse.urlencode(params)
         conn.request("POST", resource, temp_params, headers)
         response = conn.getresponse()
         data = response.read().decode('utf-8')
         params.clear()
         conn.close()
         return data
else:
    def httpGet(url,resource,params=''):
        url = 'https://' + url + resource + '?' + params
        r = requests.get(url, verify=HTTPS_VERIFY, timeout=TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return None

    def httpPost(url,resource,params):
        url = 'https://' + url + resource
        headers = {
                "Content-type" : "application/x-www-form-urlencoded",
        }
        temp_params = urllib.urlencode(params)
        r = requests.post(url, data=params, headers=headers, verify=HTTPS_VERIFY, timeout=TIMEOUT)
        print params
        print temp_params
        if r.status_code == 200:
            data = r.json()
            print data
            return data
        else:
            return None
