#!/usr/bin/python

import sys
import os
import Cookie

import sys
sys.stderr = sys.stdout

data="No Cookie"
cookie_string = ""
error = ""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    cookieJar=Cookie.SimpleCookie()
    cookieJar.load(cookie_string)
    if 'color' in cookieJar:
        data=cookieJar['color'].value
    else:
        error =  "No cookie named color"
else:
    error = "No Cookies Sent"

buf =  "The raw cookie header is " + cookie_string
buf = buf + "\nThe value of the color cookie is " + data
buf = buf + "\n" + error

print "Content-type: text/plain"
print 'Set-cookie: color=' + data + '.1'
print 'Content-length: '+str(len(buf));
print
print buf
