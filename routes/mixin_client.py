from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import requests

mixin_client = APIRouter()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

@mixin_client.options("/")
async def options_mixin_client():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "https://mixinsalamm.liara.run",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Max-Age": "86400",
        }
    )

@mixin_client.post("/")
async def create_mixin_access_token_and_url(mixin_url: str, token: str):
    method=get
    url = f"https://{mixin_url}/api/management/v1/products/"
    headers={
        'Authorization': f'Api-Key {token}'
    }
    
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        data = {
            "message": "you are connected successfully!",
            "mixin-ceredentials": {
                "mixin_url": mixin_url,
                "access_token": token
            }
        }
        
        return data
    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="we can't login with the following credentials")
    elif response.status_code == 500:
        raise HTTPException(status_code=500, detail="some error occurred... could be from server or from our request.")
    else:
        raise HTTPException(status_code=404, detail="Invalid data. could be your url or your access token")