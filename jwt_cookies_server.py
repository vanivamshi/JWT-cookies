from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from Cookie import SimpleCookie
import jwt
import time
import logging

SECRET_KEY = 'your_secret_key'
USERS = {'user1': {'id': 1, 'name': 'Alice'}, 'user2': {'id': 2, 'name': 'Bob'}}
revoked_tokens = set()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, cors=True):
        """ Helper function to set headers. """
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        if cors:
            self.send_header('Access-Control-Allow-Origin', 'http://your-allowed-domain.com')
        self.end_headers()

    def _set_cookie(self, token):
        """ Helper function to set a secure cookie. """
        self.send_header("Set-Cookie", "token={}; HttpOnly; Secure; SameSite=Strict".format(token))

    def do_GET(self):
        if 'Cookie' in self.headers:
            cookie = SimpleCookie(self.headers.get('Cookie'))
            if 'token' in cookie:
                token = cookie['token'].value
                if is_token_revoked(token):
                    self._set_headers(401)
                    self.wfile.write("Token has been revoked.")
                    return
                try:
                    decoded = jwt.decode(token, SECRET_KEY)
                    self._set_headers(200)
                    message = "Welcome back, {}!".format(decoded['name'])
                    self.wfile.write(message)
                except jwt.ExpiredSignatureError:
                    self._set_headers(401)
                    self.wfile.write("Session expired. Please log in again.")
                except jwt.DecodeError:
                    self._set_headers(401)
                    self.wfile.write("Invalid token.")
            else:
                self._send_login_page()
        else:
            self._send_login_page()

    def do_POST(self):
        # Simulate a user login (normally this would check a username and password)
        user_info = authenticate_user('user1')
        if user_info:
            token = self.generate_jwt(user_info)
            self._set_headers(200)
            self._set_cookie(token)
            self.wfile.write("Logged in successfully")
        else:
            self._set_headers(401)
            self.wfile.write("Invalid credentials.")

    def generate_jwt(self, user_info):
        """ Generate a JWT with encryption and an expiration time of 15 minutes. """
        payload = {
            "name": user_info['name'],
            "id": user_info['id'],
            "exp": int(time.time()) + 60 * 15  # 15 minutes expiry
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def _send_login_page(self):
        self._set_headers(200)
        message = """
            <html><body>
            <h2>Login</h2>
            <form method="POST" action="/">
                <button type="submit">Login</button>
            </form>
            </body></html>
        """
        self.wfile.write(message)

def authenticate_user(username):
    """ Simple user authentication. """
    if username in USERS:
        return USERS[username]
    return None

def revoke_token(token):
    """ Add the token to the revoked tokens set. """
    revoked_tokens.add(token)

def is_token_revoked(token):
    """ Check if the token is in the revoked tokens set. """
    return token in revoked_tokens

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread to allow concurrent requests. """
    pass

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = ThreadedHTTPServer(server_address, MyServer)
    print("Server running on port 8080...")
    httpd.serve_forever()
