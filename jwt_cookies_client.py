import urllib2
import cookielib

# Create a cookie jar to store cookies
cookie_jar = cookielib.CookieJar()

# Build an opener with support for cookies
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

# Send an initial request (GET request)
response = opener.open('http://localhost:8080')
print(response.read())

# Simulate logging in (POST request)
login_data = ''
login_request = urllib2.Request('http://localhost:8080', data=login_data)
login_response = opener.open(login_request)
print(login_response.read())

# Send another GET request to check if the token is saved in cookies
response = opener.open('http://localhost:8080')
print(response.read())
