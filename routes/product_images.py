from fastapi import APIRouter, HTTPException, Depends
from dependencies import AccessTokenBearer
import requests

access_token_bearer = AccessTokenBearer()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

image_router = APIRouter()

@image_router.get("/my-mixin_image")
async def get_mixin_image(
    url: str,
    mixin_product_id: int,
    mixin_page: int = 1,
    token: str = Depends(access_token_bearer)
):
    method=get
    pk=mixin_product_id
    url = f"https://{url}/api/management/v1/products/{pk}/images/"
    headers={
        'Authorization': f'Api-Key {token}'
    }
    params={
        'page': mixin_page
    }
    
    response = requests.request(method=method, url=url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()

    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="we can't login with the following credentials")
    elif response.status_code == 500:
        raise HTTPException(status_code=500, detail="some error occurred... could be from server or from our request.")
    else:
        raise HTTPException(status_code=404, detail="Invalid data. could be your url or your access token")