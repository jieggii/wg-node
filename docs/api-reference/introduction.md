# Introduction to wg-node HTTP API

> Using **wg-node** HTTP API, you can easily create and manage new WireGuard clients,
> get useful information about node.

## About wg-node API

wg-node API follows the **REST** standard.
All requests to the API are executed by means of HTTP requests.

When using wg-node API you can operate with the following objects:

* `node` - WireGuard node itself
* `api-user` - API users
* `peer` - WireGuard peers (also known as clients)

The API provides convenient methods to manipulate with them all.

!!! info

      List of available API methods can be found [here]().

## Signing API request

Important thing to know: **all API requests must be signed using API user's private key**.
What does it mean?

1. HTTP request must contain `API-User-Public-Key` header containing node API user's public key.
2. HTTP request must contain `Request-Signature` header containing signature of the request.

### How to sign request parameters?

It is really simple and also silly. The recipe:

#### Step 1. Normalize all request params

Take **path params**, **query params** and **request body** in JSON format with keys sorted as strings
and remove all spaces and newlines from them
(I call it _normalization_ in the **wg-node** source code).

For example:

* `{"boo": "hello", "aaa": 7}` -> `{"aaa":7,"boo":"hello"}`
* `{}` -> `{}`

#### Step 2. Build one string

Create a new string concatenating the following strings strictly in this order
and adding `;` separator between them:

1. HTTP method you are using in upper case (e.g. `POST`)
2. Hostname you are sending request to (e.g. `8.8.8.8` or `example.com`)
3. Normalized path params (e.g. `{"something":"123"}`)
4. Normalized query params (e.g. `{"foo":"bar"}`)
5. Normalized request body (e.g. `{"bruh":"what"}`)

For example, if we want to delete peer `peer-1` from **wg-node** running on `example.com`,
we send the following HTTP request:

> `DELETE http://example.com/peer/peer-1`.

It means we have

- HTTP method `DELETE`
- Hostname `example.com`
- Normalized path params: `{"peer_id":"peer-1"}`
- Normalized query params: `{}`
- Normalized request body: `{}`

Then the resulting concatenated string will be: `DELETE;example.com;{"peer_id":"peer-1"};{};{}`

#### Step 3. Create signature

Sign the string you got in the previous step using **RSA** algorithm and **SHA-256** as the hash method (#TODO).

#### Step 4. Set request headers

Tada!
Put your API user's public key in the `API-User-Public-Key` header and
**HEX value of signature** you've made in `Request-Signature` header and finally send your request!

### Why should all API requests to wg-node be signed?

API request params signing is a layer of security which is made to ensure
that API requests come from trusted sources and are not modified on their way by third parties.

!!! warning

    I am not a very confident developer, especially in the security area, so if you find
    this decision strange or incorrect, please feel free to discuss this topic in
    the [project issues on GitHub](https://github.com/jieggii/wg-node/issues).