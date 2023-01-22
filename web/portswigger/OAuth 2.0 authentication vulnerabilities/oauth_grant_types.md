# [OAuth grant types](https://portswigger.net/web-security/oauth/grant-types)

## OAuth grant types

## What is an OAuth grant type?
OAuth grant type (OAuth flows):
- determines the exact sequence of steps that are involved in the OAuth process.
- affects how the client application communicates with the OAuth service at each stage (how the access token itself is sent).

An OAuth service must be configured to support a particular grant tyype before a client application can initiate the corresponding flow. The client application specifies which grant type it wants to use in the initial authorization request it sends to the OAuth service.

There are several different grant types, each with varying levels of complexity and security considerations.

Most common: "authorization code" and "implicit" grant types.

## OAuth scopes
Client application has to specify which data it wants to access and what kind of operations it wants to perform.

Use the `scope` parameter of the authorization request it sends to the OAuth service.

`scope` is just an arbitrary text string => the format can vary dramatically between providers.

```
scope=contacts
scope=contacts.read
scope=contact-list-r
scope=https://oauth-authorization-server.com/auth/scopes/user/contacts.readonly
```

When OAuth is used for authentication, standardized `OpenID Connect` scopes are often used instead.

## Authorization code grant type
In short, authorization code:
- client application and OAuth service first use redirects to exchange a series of browser-based HTTP requests that initiate the flow
- The user is asked whether they consent to the requested access
- If they accept, the client application is granted an "authorization code"
- The client application then exchanges this code with the OAuth service to receive an "access token", which can use to make API calls to fetch the relevant user data.

![387fa9db551315951a88e9e0fa143e3d.png](../../../../_resources/387fa9db551315951a88e9e0fa143e3d.png)

### 1. Authorization request
```
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```
- `/authorization` endpoint may vavry between providers
- always be able to identify the endpoint based on the parameters used in the request:

parameters:
- `client_id`: unique identifier of the cilent application, granted when the client application registers with the OAuth service.
- `redirect_uri` ("callback URI" or "callback endpoint"): The URI to which the user's browser should be redirected when sending the authorization code to the client application. Many OAuth attacks are based on exploiting flows in the validation of this parameter.
- `response_type`: determines which kind of response the client application is expecting and which flow it wants to initiate. For `authorization code` grant type, the value should be `code`
- `scope`: specify which subset of the user's data the client application wants to access. May be custom scopes set by the OAuth provider, or standardized scopes defined by the OpenID Connect specification.
- `state`: unique, unguessable value tied to the current session on the client application. The OAuth service should return this exact value in the response, along with the authorization code. This parameter serves as a form of [CSRF token](https://portswigger.net/web-security/csrf/tokens) for the client application by making sure that the request to its `/callback` endpoint is from the same person who initiated the OAuth flow.
### 2. User login and consent
redirect the user to a login page.

prompted to log in to their account with the OAuth provider.

presented with a list of data that the client application wants to access, based on `scope` defined in the authorization request.

Important: once the user has approved a given scope for a client application, this step will be completed automatically as long as the user still has a valid session with the OAuth servvice.

### 3. Authorization code grant
If the user consents to the requested access, their browser will be redirected to the `/callback` endpoint that was specified in the `redirect_uri` parameter of the authorization request.

...
Trang portswigger ghi đầy đủ quá, đọc ở đó luôn thôi.