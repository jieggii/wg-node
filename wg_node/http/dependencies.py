import json
from http import HTTPStatus
from typing import Any, NoReturn

import rsa
from fastapi import Header, HTTPException, Request
from typing_extensions import Annotated

from wg_node.database import APIUser

_SIGNED_PARTS_SEPARATOR = b";"


def _normalize(obj: dict[Any, Any]) -> bytes:
    """
    Normalizes dict object to json bytes.
    >>> _normalize({"foo": "bar", "x": "y"})
    >>> b'{"foo":"bar","x":"y"}'
    """
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()


async def verify_request_signature(
    request: Request,
    request_signature: Annotated[str, Header(alias="Request-Signature")],
    api_user_public_key: Annotated[str, Header(alias="API-User-Public-Key")],
) -> APIUser | NoReturn:
    user = await APIUser.find_one(APIUser.public_key == api_user_public_key)
    if not user:
        raise HTTPException(HTTPStatus.FORBIDDEN, "user with such public key was not found")

    method = request.method
    hostname = request.url.hostname
    path_params = request.path_params
    query_params = dict(request.query_params)

    raw_body = await request.body()
    body = await request.json() if raw_body else {}

    method_bytes = method.encode()
    hostname_bytes = hostname.encode()
    path_params_bytes = _normalize(path_params)
    query_params_bytes = _normalize(query_params)
    body_bytes = _normalize(body)

    # print(f"RAW:\n{method=}\n{hostname=}\n{path_params=}\n{query_params=}\n{body=}\n", flush=True)
    # print(
    #     f"NORMALIZED:\n{method_bytes=}\n{hostname_bytes=}\n{path_params_bytes=}\n{query_params_bytes=}\n{body_bytes=}\n",
    #     flush=True,
    # )

    signed_bytes = (
        method_bytes
        + _SIGNED_PARTS_SEPARATOR
        + hostname_bytes
        + _SIGNED_PARTS_SEPARATOR
        + path_params_bytes
        + _SIGNED_PARTS_SEPARATOR
        + query_params_bytes
        + _SIGNED_PARTS_SEPARATOR
        + body_bytes
    )
    try:
        signature_hex = bytes.fromhex(request_signature)
    except ValueError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid request signature")

    try:
        rsa.verify(
            message=signed_bytes,
            signature=signature_hex,
            pub_key=rsa.PublicKey.load_pkcs1(
                b"-----BEGIN RSA PUBLIC KEY-----\n" + user.public_key.encode() + b"\n-----END RSA PUBLIC KEY-----"
            ),
        )
    except rsa.VerificationError:
        raise HTTPException(HTTPStatus.FORBIDDEN, "invalid Request-Signature header")

    return user
