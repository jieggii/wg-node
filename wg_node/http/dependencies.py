import json
import rsa

from http import HTTPStatus
from fastapi import Header, HTTPException, Request
from typing_extensions import Annotated

from wg_node.docker_secrets import read_docker_secret

# read node master's public keys from the docker secret file
master_public_keys = read_docker_secret("node_master_public_keys").split("\n")
if not master_public_keys:
    raise RuntimeError(
        "no node master's public keys indicated in the `node_master_public_keys` docker secret",
    )


async def validate_request_signature(
        request: Request,
        request_signature: Annotated[str, Header(alias="Request-Signature", title="Request signature")],
        master_public_key: Annotated[str, Header(alias="Master-Public-Key", title="Master public key")]
):
    """
    Validates request params (path params, query params and request body) signature header (Request-Signature).
    """

    # master public key is provided by the client in the matching header
    # only for performance purposes, so we don't need to verify request params signature
    # with all stored master public keys
    if master_public_key not in master_public_keys:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="unknown master public key"
        )

    path_params = request.path_params
    query_params = dict(request.query_params)
    body = await request.body()

    # converting path params and query params (dict) to json bytes
    # e.g. {"foo": "bar", "x": "y"} to b'{"foo":"bar","x":"y"}'
    path_params_bytes = json.dumps(
        path_params, separators=(",", ":"), sort_keys=False
    ).encode("utf-8")
    query_params_bytes = json.dumps(
        query_params, separators=(",", ":"), sort_keys=False
    ).encode("utf-8")

    # signed bytes are concatenation of path params, query params and body
    signed_bytes = path_params_bytes + query_params_bytes + body
    try:
        rsa.verify(
            message=signed_bytes,
            signature=request_signature.encode(),
            pub_key=rsa.PublicKey.load_pkcs1(master_public_key.encode()),
        )
    except rsa.VerificationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="invalid Request-Signature header"
        )
    return request_signature
