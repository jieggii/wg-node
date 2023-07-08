# Manage your wg-node instance

> When everything is set up properly and already running, it is time to send requests to the
> **wg-node** instance and have some fun.

## Sending API request

!!! info

    Using **wg-node** HTTP API, you can easily create and manage new WireGuard clients,
    get useful information about node.

Important thing to know: **all API requests must be signed using API user's private key**.
What does it mean?

1. HTTP request must contain `API-User-Public-Key` header containing (you won't believe) node client's public key.
2. HTTP request must contain `Request-Signature` header containing (you won't believe) request parameters'
   signature.

### How to sign request parameters?

It is really simple and also silly. The recipe:

#### Step 1. Normalize all request params

Take **path params**, **query params** and **request body** in JSON format as strings
and remove all spaces and newlines from them
(I call it _normalization_ in the **wg-node** source code).
For example: `{"foo": "bar", "meow": 7}` -> `{"foo":"bar","meow":7}`

#### Step 2. Concatenate strings you got

Concatenate the following strings strictly in this order:

1. HTTP method you are using (e.g. `POST`)
2. Hostname you are sending request to (e.g. `8.8.8.8`)
3. Normalized path params
4. Normalized query params
5. Normalized request body

And add `;` separator between them.

For example, if we want to delete peer `peer-1` from **wg-node** running on `1.1.1.1`,
we send the following HTTP request:

> `DELETE http://1.1.1.1/peer/peer-1`.

It means we have

- HTTP method `DELETE`
- Hostname `1.1.1.1`
- Normalized path params: `{"peer_id":"peer-1"}`
- normalized query params: `{}`
- normalized request body: `{}`

Then the resulting concatenated string will be: `DELETE;1.1.1.1;{"peer_id":"peer-1"};{};{}`

#### Step 3. Create signature

Sign the string you got in the previous step using **RSA** algorithm and **SHA-1** as the hash method (#TODO).

#### Step 4. Set request headers

Tada!
Put your API user's public key in the `API-User-Public-Key` header and
HEX value of signature you've made in `Request-Signature` header and finally send your request!

!!! info

    Please refer to [API reference]() to get more information about **wg-node** API and API methods.

### Why should all API requests to wg-node be signed?

API request params signing is a layer of security which is made to ensure
that API requests come from trusted sources.

!!! warning

    I am not a very confident developer, especially in the security area, so, if you find
    this decision strange or incorrect, please feel free to discuss this topic in
    the [project issues on GitHub](https://github.com/jieggii/wg-node/issues).