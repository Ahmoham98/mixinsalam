from fastapi import APIRouter, HTTPException, status
import requests

mixin_client = APIRouter()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

@mixin_client.post("/")
async def create_mixin_access_token_and_url(mixin_url: str, token: str):
    method=get
    pk = 1
    url = f"https://{mixin_url}/api/management/v1/products/{pk}"
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Api-Key {token}'
    }
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        pass
    else: 
        raise HTTPException(status_code=404, detail="Invalid data. could be your url or your access token")

    data = {
        "message": "you are connected successfully!",
        "mixin-ceredentials": {
            "mixin_url": mixin_url,
            "access_token": token
        }
    }
    
    return data