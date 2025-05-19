from fastapi import APIRouter


mixin_client = APIRouter()


def store_mxin_url_and_mixin_access_token(mixin_url: str, mixin_access_token: str):
    mixin_url = mixin_url
    mixin_access_token = mixin_access_token


@mixin_client.post()
async def create_mixin_access_token_and_url(mixin_url: str, access_token: str):
    
    #store mixin url and access_token for global use
    store_mxin_url_and_mixin_access_token(mixin_url, access_token)