# JWT-cookies

A simple program to store JWT cookies at server end with the following,

1. JWT Authentication - The server authenticates users by generating a JSON Web Token (JWT) after successful login. The token is signed with a secret key (HS256 algorithm) and contains user-specific data like their name, ID, and token expiration time.

2. Token Expiry and Session Management - JWT tokens are generated with a 15-minute expiration (exp field in the payload). This ensures that the token is valid only for a specific period, and users will need to log in again once the token expires.

3. Secure Cookie Handling - The JWT token is stored in a secure cookie with the following security attributes - [a]HttpOnly: Prevents client-side scripts from accessing the cookie, mitigating XSS (Cross-Site Scripting) attacks. [b] Secure: Ensures that cookies are sent only over HTTPS connections, enhancing security. [c] SameSite=Strict: Prevents cookies from being sent with cross-site requests, protecting against CSRF (Cross-Site Request Forgery) attacks.

4. CORS (Cross-Origin Resource Sharing) and CSRF Protection - CORS protection is enabled by restricting cross-origin requests to a specific allowed domain (Access-Control-Allow-Origin header). CSRF protection is partially handled by restricting cookie use with the SameSite=Strict attribute, reducing the risk of unauthorized cross-site access.

5. Support for Multiple Users - The program supports multiple users with a dictionary of users (USERS). Each user is identified by a unique ID and name, and their information is embedded in the JWT token after successful login.

6. Token Encryption (Signing) - The JWT payloads are signed using the HS256 algorithm, ensuring that the token's contents are tamper-proof and can be verified by the server using the secret key.

7. Token Revocation Mechanism - The server includes a mechanism to revoke tokens. If a token is revoked, it is added to a set of revoked tokens, and any subsequent requests with that token will be denied. This allows the server to invalidate tokens, even if they haven't expired.

8. Multi-Threading for Concurrent Requests - The server uses multi-threading (ThreadingMixIn) to handle multiple client requests concurrently. This allows the server to efficiently process several requests at the same time, improving scalability and responsiveness.

9. Basic User Authentication - The server simulates user authentication by checking the username from a predefined set of users (USERS). This can be extended to include proper password verification or other authentication mechanisms.

10. Basic HTTP Interface - The program implements basic GET and POST handlers for client interaction. The GET request checks for the token in cookies, while the POST request simulates user login and sets the token in a secure cookie.

11. Logging - Basic logging is implemented to track important events like user login, token creation, and server responses, providing visibility into the server's operations.

12. Custom HTML Response - When there is no valid token or session, the server returns a simple HTML-based login form. This makes it easy to extend and add a web interface if needed.
