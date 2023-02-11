# [OAuth 2.0 authentication vulnerabilities](https://portswigger.net/web-security/oauth)

## Labs

- appentice
  - [1. Authentication bypass via OAuth implicit flow](./lab/1.%20Authentication%20bypass%20via%20OAuth%20implicit%20flow.md)

- practitioner
  - [2. Forced OAuth profile linking](./lab/2.%20Forced%20OAuth%20profile%20linking.md): no state field
  - [3. OAuth account hijacking via redirect_uri](./lab/3.%20OAuth%20account%20hijacking%20via%20redirect_uri.md): arbitrary redirect_uri
  - [4. Stealing OAuth access tokens via an open redirect](./lab/4.%20Stealing%20OAuth%20access%20tokens%20via%20an%20open%20redirect.md): whitelist-based filter redirect_uri

## Summary

### OAuth 2.0 grant type

#### I. Authorization code grant type

![authorization.png](./img/oauth-authorization-code-flow.jpg)

##### 1. Authorization request

```http
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

- `client_id`: Mandatory parameter containing the unique identifier of the client application. This value is generated when the client application registers with the OAuth service.
- `redirect_uri`: The URI to which the user's browser should be redirected when sending the authorization code to the client application. This is also known as the "callback URI" or "callback endpoint".
- `response_type`: Determines which kind of response the client application is expecting and, therefore, which flow it wants to initiate. For the authorization code grant type, the value should be code.
- `scope`: Used to specify which subset of the user's data the client application wants to access. Note that these may be custom scopes set by the OAuth provider or standardized scopes defined by the OpenID Connect specification.
- `state`: csrf token, making sure that the request to its /callback endpoint is from the same person who initiated the OAuth flow.

##### 2. User login and consent

##### 3. Authorization code grant

```http
GET /callback?code=a1b2c3d4e5f6g7h8&state=ae13d489bd00e3c24 HTTP/1.1
Host: client-app.com
```

##### 4. Access token request

All communication from this point on takes place in a secure back-channel and, therefore, cannot usually be observed or controlled by an attacker.

```http
POST /token HTTP/1.1
Host: oauth-authorization-server.com
…
client_id=12345&client_secret=SECRET&redirect_uri=https://client-app.com/callback&grant_type=authorization_code&code=a1b2c3d4e5f6g7h8
```

- `client_secret`: The client application must authenticate itself by including the secret key that it was assigned when registering with the OAuth service.
- `grant_type`: Used to make sure the new endpoint knows which grant type the client application wants to use. In this case, this should be set to authorization_code.

##### 5. Access token grant

The OAuth service will validate the access token request. If everything is as expected, the server responds by granting the client application an access token with the requested scope.

```json
{
    "access_token": "z0y9x8w7v6u5",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid profile",
    …
}
```

##### 6. API call

```http
GET /userinfo HTTP/1.1
Host: oauth-resource-server.com
Authorization: Bearer z0y9x8w7v6u5
```

##### 7. Resource grant

```json
{
    "username":"carlos",
    "email":"carlos@carlos-montoya.net",
    …
}
```

#### II. Implicit grant type

![implicit.png](./img/oauth-implicit-flow.jpg)

##### 1. Authorization request_

```http
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=token&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

- `response_type`: token

##### 2. User login and consent_

##### 3. Access token grant

instead of sending a query parameter containing an authorization code, it will send the access token and other token-specific data as a URL fragment.

```http
GET /callback#access_token=z0y9x8w7v6u5&token_type=Bearer&expires_in=5000&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: client-app.com
```

##### 4. API call

Unlike in the authorization code flow, this also happens via the browser.

```http
GET /userinfo HTTP/1.1
Host: oauth-resource-server.com
Authorization: Bearer z0y9x8w7v6u5
```

##### 5. Resource grant

```json
{
    "username":"carlos",
    "email":"carlos@carlos-montoya.net"
}
```
