# Manage your wg-node instance

> When everything is set up properly and already running, it is time to send requests to the
> **wg-node** instance and have some fun.

## Sending API request

> Using **wg-node** HTTP API, you can easily create and manage new WireGuard clients,
> get useful information about node.

Important thing to know: **all API requests must be signed using node client's private key**.
What does it mean?

1. HTTP request must contain `Client-Public-Key` header containing (you won't believe) node client's public key.
2. HTTP request must contain `Params-Signature` header containing (you won't believe) request parameters' signature.

### How to sign request parameters?

It is really simple and also silly. The recipe:

1. Take **path params**, **query params** and **request body** (order is important)
   in JSON format and remove all spaces and newlines from them. For example,
   `{"foo": "bar", "meow": 7}` -> `{"foo":"bar","meow":7}` (I call it _normalization_ in the **wg-node** source code).
2. Concatenate normalized JSONs like usual strings. For example, if we have
    * normalized path params: `{}`
    * normalized query params: `{}`
    * normalized request body: `{"client_id":"client-1"}`

      then the concatenated string will be: `{}{}{"client_id":"client-1"}`

3. Sign the string we got in the previous step using **RSA** algorithm and **SHA-1** as the hash method (#TODO).
4. Tada! Put your node client's public key in the `Client-Public-Key` header and
   HEX value of signature in `Params-Signature` header and finally send your request!

> Please refer to [API reference]() to get more information about **wg-node** API.

## Why should all API requests to wg-node be signed?

API request params signing is a layer of security which is made to ensure
that API requests come from trusted sources.

> I am not a very confident developer, especially in the security area, so, if you find
> this decision strange or incorrect, please feel free to discuss this topic in
> the [project issues on GitHub](https://github.com/jieggii/wg-node/issues).