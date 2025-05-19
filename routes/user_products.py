from fastapi import APIRouter, HTTPException, status
import requests
import json

product_router = APIRouter()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


@product_router.get("/")
async def get_all_product(url: str, token: str, page: int):
    #get all products from mixin
    
    method=get
    url=f"https://{url}/api/management/v1/products/"
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Api-Key {token}'
    }
    params={
        'page': page
    }
    
    response = requests.request(method=method, url=url, params=params, headers=headers)
    
    if response.status_code == 200:
        response = response.json()
        
        mixin_product_data = response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
    
    #get all products form basalam
    


@product_router.get("/{product_id}")
async def get_async_product():
    pass