from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
import requests
import json

from dependencies import EqualityChecker
from database import get_session
from schema.mixin import MixinCreate, MixinAddToDatabase
from schema.basalam import BasalamCreate
from controllers.products import ProductController


post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


get_products_equality_checker = EqualityChecker(handler=get, mixin_body="some random data dict", basalam_body='some random data dict')
post_products_equality_checker = EqualityChecker(handler=post, mixin_body="some random data dict", basalam_body='some random data dict')
put_products_equality_checker = EqualityChecker(handler=put, mixin_body="some random data dict", basalam_body='some random data dict')

product_router = APIRouter()


@product_router.get("/my-mixin-products")
async def get_all_mixin_products(url: str, mixin_token: str, mixin_page: int = 1):
    mixin_method=get
    mixin_url=f"https://{url}/api/management/v1/products/"
    mixin_headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Api-Key {mixin_token}'
    }
    mixin_params={
        'page': mixin_page
    }
    
    response = requests.request(method=mixin_method, url=mixin_url, params=mixin_params, headers=mixin_headers)
    
    if response.status_code == 200:
        response = response.json()
        
        mixin_body = response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
    
    return mixin_body


@product_router.get("/my-basalam-products")
async def get_all_basalam_products(basalam_page: int = 1):
    method= get
    url="https://core.basalam.com/v3/products"
    headers={
        'Accept': 'application/json'
    }
    params={
        "page": basalam_page
    }
    
    response = requests.request(method=method, url=url, headers=headers, params=params)
    
    if response.status_code == 200:
        response = response.json()
        
        basalam_body = response
    else: 
        raise HTTPException(status_code=404, detail="we can't connect to the provider")
    
    return basalam_body


@product_router.get("/get-if-equal")
async def get_all_product(url: str, mixin_token: str, mixin_page: int, basalam_token: str, basalam_page: int):
    #get all products from mixin
    
    mixin_method=get
    mixin_url=f"https://{url}/api/management/v1/products/"
    mixin_headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Api-Key {mixin_token}'
    }
    mixin_params={
        'page': mixin_page
    }
    
    response = requests.request(method=mixin_method, url=mixin_url, params=mixin_params, headers=mixin_headers)
    
    if response.status_code == 200:
        response = response.json()
        
        mixin_body = response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
    
    #get all products form basalam
    
    method= get
    url="https://core.basalam.com/v3/products"
    headers={
        'Accept': 'application/json'
    }
    params={
        "page": basalam_page
    }
    
    response = requests.request(method=method, url=url, headers=headers, params=params)
    
    if response.status_code == 200:
        response = response.json()
        
        basalam_body = response
    else: 
        raise HTTPException(status_code=404, detail="we can't connect to the provider")
    
    result = await EqualityChecker(handler=get, mixin_body=mixin_body, basalam_body=basalam_body)
    
    if result:
        
        data = {
            "your product_in_basalam": {
                basalam_body
            },
            "mixin_product_in_mixin": {
                mixin_body
            }
        }
        
        return data
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="your product in mixin and basalam are not the same. go to the update secrion to make them same for you.")


@product_router.get("/mixin/{mixin_product_id}")
async def get_async_product(
    mixin_url: str,
    mixin_token: str,
    mixin_product_id: int,
    _: bool = Depends(get_products_equality_checker)
):
    method = get
    pk = mixin_product_id
    url=f"https://{mixin_url}/api/management/v1/products/{pk}"
    headers={
        'Authorization': f'Api-Key {mixin_token}'
    }
    
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        mixin_body = response.json()
        return mixin_body
    elif response.status_code == 403:
        raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
    elif response.status_code == 500:
        raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting mixin product with given id. check if you are connected to mixin website")


@product_router.get("/basalam/{basalam_product_id}")
async def get_async_product(
    basalam_product_id: int,
    _: bool = Depends(get_products_equality_checker)
):
    method= get
    url=f"https://core.basalam.com/v3/products/{basalam_product_id}"
    headers={
        'Accept': 'application/json',
        'prefer': 'minimal'
    }
    
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        basalam_body = response.json()
        
        return basalam_body
        
    elif response.status_code == 403:
        raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
    elif response.status_code == 500:
        raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")



@product_router.post("/mixin")
async def create_mixin_product(
    *,
    session: AsyncSession = Depends(get_session),
    mixin_url: str,
    mixin_token: str,
    data: MixinCreate,
    _: bool = Depends(get_products_equality_checker)
):
    method = post
    url=f"https://{mixin_url}/api/management/v1/products/"
    headers={
        'Authorization': f'Api-Key {mixin_token}'
    }
    body={
        data
    }
    response = requests.request(method=method, url=url, headers=headers, data=body)
    
    if response.status_code == 200:
        mixin_body = response.json()
        
        #make the data ready to be created in the database too
        new_product = MixinAddToDatabase()
        new_product.mixin_id = mixin_body['id']
        new_product.name = data['name']
        new_product.price = data['price']
        
        return mixin_body
    
    elif response.status_code == 403:
        raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
    elif response.status_code == 500:
        raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting mixin product with given id. check if you are connected to mixin website")

    
    

@product_router.post("/basalam/{vendor_id}")
async def get_async_product(
    vendor_id: int,
    data: BasalamCreate,
    _: bool = Depends(get_products_equality_checker)):
    method= post
    url=f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
    headers={
        'Accept': 'application/json',
        'prefer': 'minimal'
    }
    body={
        data
    }
    response = requests.request(method=method, url=url, headers=headers, data=body)
    
    if response.status_code == 200:
        basalam_body = response.json()
        
        return basalam_body
        
    elif response.status_code == 403:
        raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
    elif response.status_code == 500:
        raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")

    

@product_router.put("/mixin/{mixin_product_id}")
async def get_async_product(_: bool = Depends(get_products_equality_checker)):
    pass

@product_router.put("/basalam/{basalam_product_id}")
async def get_async_product(_: bool = Depends(get_products_equality_checker)):
    pass


