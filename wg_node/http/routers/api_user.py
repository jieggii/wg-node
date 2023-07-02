from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from wg_node.database import APIUser
from wg_node.http.dependencies import verify_request_signature

router = APIRouter(prefix="/api-user")


class APIUserCreateParams(BaseModel):
    public_key: str


class APIUserCreateResponse(BaseModel):
    pass


@router.post("/", summary="creates new API user")
async def api_user_create(
    params: APIUserCreateParams, current_user: APIUser = Depends(verify_request_signature)
) -> APIUserCreateResponse:
    if not current_user.is_root_user:
        raise HTTPException(HTTPStatus.FORBIDDEN, "you have no right to create new API users")
    user = APIUser(public_key=params.public_key)
    await user.insert()
    return APIUserCreateResponse()


class APIUserDeleteResponse(BaseModel):
    pass


@router.delete("/{public_key}/", summary="deletes existing API user")
async def api_user_delete(
    public_key: str, current_user: APIUser = Depends(verify_request_signature)
) -> APIUserDeleteResponse:
    if not current_user.is_root_user:
        raise HTTPException(HTTPStatus.FORBIDDEN, "you have no right to delete users")
    user = await APIUser.find_one(APIUser.public_key == public_key)
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, "user not found")
    await user.delete()
    return APIUserDeleteResponse()
