
from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.mixin import MixinAddToDatabase, MixinCreate
from schema.basalam import BasalamCreate, BaslaamUpdate

from fastapi import HTTPException, status
import requests

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

class ProductController:
    def __init__(self):
        pass
    
    async def get_mixin_products(self, url: str, mixin_token: str, mixin_page: int):
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
            return mixin_body
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
    
    async def get_basalam_products(self, basalam_page: int):
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
            return basalam_body
        else:
            raise HTTPException(status_code=404, detail="we can't connect to the provider")
    
    async def get_mixin_product(self, mixin_url: str, mixin_product_id: int, mixin_token: str ):
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
    
    async def get_basalam_product(self, basalam_product_id: int):
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
    
    async def create_mixin_product(self, url: str, mixin_token: str, mixin_body: MixinCreate):
        mixin_method=post
        mixin_url=f"https://{url}/api/management/v1/products/"
        mixin_headers={
            'Authorization': f'Api-Key {mixin_token}'
        }
        body=mixin_body
        response = requests.request(method=mixin_method, url=mixin_url, headers=mixin_headers, data=body)
        
        if response.status_code == 200:
            response = response.json()
            
            mixin = response
            return mixin
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
        
    async def create_basalam_product(self, vendor_id: int, basalam_body: BasalamCreate):
        method=post
        url=f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
        body=basalam_body
        data = {
        "name": "string",
        "photo": 0,
        "photos": [
            0
        ],
        "video": 0,
        "brief": "string",
        "description": "string",
        "order": 0,
        "category_id": 0,
        "status": 0,
        "preparation_days": 0,
        "keywords": [
            "string"
        ],
        "weight": 0,
        "package_weight": 0,
        "price": 0,
        "stock": 0,
        "shipping_city_ids": [
            0
        ],
        "shipping_method_ids": [
            0
        ],
        "wholesale_prices": [
            {
            "price": 10000,
            "min_quantity": 2
            }
        ],
        "product_attribute": [
            {
            "attribute_id": 0,
            "value": "string",
            "selected_values": [
                0
            ]
            }
        ],
        "virtual": True,
        "variants": [
            {
            "price": 0,
            "stock": 0,
            "sku": "string",
            "properties": [
                {
                "value": "string",
                "property": "string"
                }
            ]
            }
        ],
        "shipping_data": {
            "illegal_for_iran": True,
            "illegal_for_same_city": True
        },
        "unit_quantity": 0,
        "unit_type": 0,
        "sku": "string",
        "packaging_dimensions": {
            "height": 0,
            "length": 0,
            "width": 0
        },
        "is_wholesale": True
        }
        
        response = requests.request(method=method, url=url, data=data)
        
        if response.status_code == 200:
            basalam_body = response.json()
            
            return basalam_body
            
        elif response.status_code == 403:
            raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
        elif response.status_code == 500:
            raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")
    
    async def update_mixin_product(self, url: str, mixin_token: str, mixin_product_id: int, mixin_body: MixinCreate):
        mixin_method=put
        pk=mixin_product_id
        mixin_url=f"https://{url}/api/management/v1/products/{pk}"
        mixin_headers={
            'Authorization': f'Api-Key {mixin_token}'
        }
        body=mixin_body
        response = requests.request(method=mixin_method, url=mixin_url, headers=mixin_headers, data=body)
        
        if response.status_code == 200:
            response = response.json()
            
            mixin = response
            return mixin
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting all mixin products. check if you are connected to mixin website")
    
    async def update_basalam_product(self, vendor_id: int, basalam_body: BaslaamUpdate):
        method=patch
        url=f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
        body=basalam_body
        data = {
                "data": [
                    {
                    "id": 0,
                    "name": "string",
                    "price": 0,
                    "order": 0,
                    "stock": 0,
                    "status": 0,
                    "preparation_days": 0,
                    "variants": [
                        {
                        "id": 0,
                        "price": 0,
                        "stock": 0
                        }
                    ],
                    "product_attribute": [
                        {
                        "attribute_id": 0,
                        "value": "string",
                        "selected_values": [
                            0
                        ]
                        }
                    ],
                    "shipping_data": {
                        "illegal_for_iran": True,
                        "illegal_for_same_city": True
                    }
                    }
                ]
                }
        
        response = requests.request(method=method, url=url, data=data)
        
        if response.status_code == 200:
            basalam_body = response.json()
            
            return basalam_body
            
        elif response.status_code == 403:
            raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
        elif response.status_code == 500:
            raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")
    
    async def delete_mixin_product(self, mixin_product_id: int, url: str, mixin_token: str ):
        method=delete
        pk = mixin_product_id
        url=f"https://{url}/api/management/v1/products/{pk}"
        headers={
            'Authorization': f'Api-Key {mixin_token}'
        }
        
        response = requests.request(method=method, url=url, headers=headers)
        
        if response.status_code == 200:
            return "success!"
        elif response.status_code == 403:
            raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
        elif response.status_code == 500:
            raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting mixin product with given id. check if you are connected to mixin website")
    
    async def is_equal(self, basalam_product_id: int, mixin_url: str, mixin_token: str , mixin_product_id: int):
        basalam_product = await self.get_basalam_product(basalam_product_id=basalam_product_id)
        mixin_product = await self.get_mixin_product(mixin_url=mixin_url, mixin_product_id=mixin_product_id, mixin_token=mixin_token)
        
        if mixin_product['name'] != basalam_product['title']:
            return False
        elif mixin_token['price'] != basalam_product['price']:
            return False
        else:
            return True