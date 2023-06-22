import json
from http import HTTPStatus

import rsa
from fastapi import Header, HTTPException, Request
from loguru import logger
from typing_extensions import Annotated

from wg_node.docker_secrets import read_node_clients_public_keys

node_clients_public_keys = read_node_clients_public_keys()

logger.info(f"loaded {len(node_clients_public_keys)} node clients public keys")


def _normalize_dict(obj: dict) -> bytes:
    """
    Normalizes dict object to json bytes.
    >>> _normalize_dict({"foo": "bar", "x": "y"})
    >>> b'{"foo":"bar","x":"y"}'
    """
    return json.dumps(obj, separators=(",", ":"), sort_keys=False).encode()


async def verify_request(
        request: Request,
        request_params_signature: Annotated[str, Header(alias="Request-Params-Signature")],
        client_public_key: Annotated[str, Header(alias="Client-Public-Key")],
):
    """
    Authenticates a client:
    - Ensures that client public key (from Client-Public-Key header) is known
    - Validates request params signature (which is indicated in Request-Params-Signature header)
    """

    # client public key is provided by the client in the Client-Public-Key header
    # only in performance purposes, so we don't need to try verifying request params signature
    # with all stored clients public keys
    if client_public_key not in node_clients_public_keys:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="unknown client public key")

    path_params = request.path_params
    query_params = dict(request.query_params)

    # this is very smelly code, I know, that there certainly must be something different...
    for key, value in query_params.items():
        if query_params[key] == "True":
            query_params[key] = True
        if query_params[key] == "False":
            query_params[key] = False
        # try:
        #     query_params[key] = int(value)
        # except ValueError:
        #     continue

    body = await request.json()

    # converting path params, query params and request body to normalized json bytes
    # e.g. {"foo": "bar", "x": "y"} -> b'{"foo":"bar","x":"y"}'
    path_params_bytes = _normalize_dict(path_params)
    query_params_bytes = _normalize_dict(query_params)
    body_bytes = _normalize_dict(body)

    # signed bytes are concatenation of path params, query params and request body
    signed_bytes = path_params_bytes + query_params_bytes + body_bytes
    try:
        rsa.verify(
            message=signed_bytes,
            signature=bytes.fromhex(request_params_signature),
            pub_key=rsa.PublicKey.load_pkcs1(
                b"-----BEGIN RSA PUBLIC KEY-----\n" + client_public_key.encode() + b"\n-----END RSA PUBLIC KEY-----"
            ),
        )
    except rsa.VerificationError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid request signature")
