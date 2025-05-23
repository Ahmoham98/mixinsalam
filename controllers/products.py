
from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.mixin import MixinAddToDatabase, MixinCreate
from schema.basalam import BasalamCreate, BaslaamUpdate

from fastapi import HTTPException, status, UploadFile
import requests

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

class ProductController:                # Need to assign real body data from schemas after testing the endpoint using inserted sample data
    def __init__(self):
        pass
    
    async def get_mixin_products(url: str, mixin_token: str, mixin_page: int):
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
    
    async def get_basalam_products(token: str, vendor_id: int, basalam_page: int):
        method= get
        url=f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
        headers={
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
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
    
    async def get_mixin_product(mixin_url: str, mixin_product_id: int, mixin_token: str ):
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
    
    async def get_basalam_product(token: str, basalam_product_id: int):
        method= get
        url=f"https://core.basalam.com/v3/products/{basalam_product_id}"
        headers={
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
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
    
    async def create_mixin_product(url: str, mixin_token: str, mixin_body: MixinCreate):
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
        
    async def create_basalam_product(token: str ,vendor_id: int, basalam_body: BasalamCreate, photo: UploadFile = None):
        method=post
        url=f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
        body=basalam_body
        headers={
            'Authorization': f'Bearer {token}'
        }
        
        files = {}
        if photo: 
            files['photo'] = (photo.filename, await photo.read(), photo.content_type)
        
        
        response = requests.request(method=method, url=url, data=body, headers=headers, files=files)
        
        if response.status_code == 200:
            basalam_body = response.json()
            
            return basalam_body
            
        elif response.status_code == 403:
            raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
        elif response.status_code == 500:
            raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")
    
    async def update_mixin_product(url: str, mixin_token: str, mixin_product_id: int, mixin_body: MixinCreate):
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
    
    @staticmethod
    async def update_basalam_product(token: str ,product_id: int, basalam_body: dict, photo: UploadFile = None):
        method=patch
        url=f"https://core.basalam.com/v3/products/{product_id}"
        headers={
            'Authorization': f'Bearer {token}'
        }
        body= basalam_body
        
        files = {}
        if photo: 
            files['photo'] = (photo.filename, await photo.read(), photo.content_type)
        
        response = requests.request(method=method, url=url, data=body, headers=headers, files=files)
        
        return {"data": {  
            "status_code": response.status_code,
            "response": response.json()
        }}
        
        if response.status_code == 200:
            basalam_body = response.json()
            
            return basalam_body
            
        elif response.status_code == 403:
            raise HTTPException(status_code=404, detail="403 forbidden error occurred. perhaps whe don't have access to the resource for now! check the request and parameters again for future request.")
        elif response.status_code == 500:
            raise HTTPException(status_code=404, detail="500 Internal server error occurred. It seems we have problem in request or some issue or problem from the server. check the request and parameters again for future request.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for getting basalam product with given id. check if you are connected to basalam website")
    
    async def delete_mixin_product(mixin_product_id: int, url: str, mixin_token: str ):
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
    
    async def is_equal(basalam_product_id: int, mixin_url: str, mixin_token: str , mixin_product_id: int):
        basalam_product = await self.get_basalam_product(basalam_product_id=basalam_product_id)
        mixin_product = await self.get_mixin_product(mixin_url=mixin_url, mixin_product_id=mixin_product_id, mixin_token=mixin_token)
        
        if mixin_product['name'] != basalam_product['title']:
            return False
        elif mixin_token['price'] != basalam_product['price']:
            return False
        else:
            return True