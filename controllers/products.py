
from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.mixin import MixinAddToDatabase, MixinCreate
from schema.basalam import BasalamCreate, BaslaamUpdate

from fastapi import HTTPException, status, UploadFile
import requests
import json
import httpx

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
        mixin_url=f"https://{url}/api/management/v1/products/"
        mixin_headers={
            'Authorization': f'Api-Key {mixin_token}'
        }
        mixin_body = mixin_body.model_dump()
        body=mixin_body
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url=mixin_url, headers=mixin_headers, json=body)
        
        if response.status_code == 201:
            response = response.json()
            
            mixin = response
            return mixin
        elif response.status_code == 401:
            return {
                "result": {
                    "message": "you are 401 and you are not Authorized to have access",
                    "response": response.json()
                }
            }
        elif response.status_code == 403:
            return {
                "result": {
                    "message": "you have 403 forbidden",
                    "response": response.json()
                }
            }
        elif response.status_code == 500:
            return {
                "result": {
                    "message": "you have 500 internal server error from mixin server",
                    "response": response.json()
                }
            }
        else:
            return {
                "result": {
                    "message": "some error occurred, it may be from the request, check your request body or params",
                    "response": response.json()
                }
            } 
    
    @staticmethod
    async def upload_product_image(token: str, product_id: int, photo: UploadFile):
        url = "https://core.basalam.com/v3/product-photos/upload"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "photo": (photo.filename, await photo.read(), photo.content_type),
            "product_id": (None, str(product_id))  # Notice this is form field, not file
        }

        response = requests.post(url, headers=headers, files=files)
        return {
            "status_code": response.status_code,
            "response": response.json()
        }
        

    @staticmethod
    async def upload_image(token: str, file: UploadFile):
        url = "https://uploadio.basalam.com/v3/files"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        file_content = await file.read() 
        
        async with httpx.AsyncClient() as client:
            files_payload = {
                "file": (file.filename, file_content, file.content_type), 
                "file_type": (None, "product.photo")
            }
            
            response = await client.post(url, headers=headers, files=files_payload)
            response.raise_for_status() 
            
            print(f"Response from Basalam upload API: {response.status_code} - {response.json()}")

        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    @staticmethod
    async def create_basalam_product(token: str, vendor_id: int, body: dict):
        url = f"https://core.basalam.com/v4/vendors/{vendor_id}/products"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code == 201:
            return response.json()  # Includes the new product’s ID
        elif response.status_code == 403:
            raise HTTPException(403, "Forbidden – check your token or permissions")
        else:
            raise HTTPException(response.status_code, response.text)
    
    async def update_mixin_product(url: str, mixin_token: str, mixin_product_id: int, mixin_body: MixinCreate):
        pk=mixin_product_id
        mixin_url=f"https://{url}/api/management/v1/products/{pk}"
        mixin_headers={
            'Authorization': f'Api-Key {mixin_token}'
        }
        
        mixin_body = mixin_body.model_dump()
        
        body=mixin_body
        
        
        async with httpx.AsyncClient() as client:
            response = await client.put(url=mixin_url, headers=mixin_headers, json=body, follow_redirects=True)
        
        
        if response.status_code == 200 :
            response = response.json()
            return response
        if response.status_code == 404 :
            response = response.json()
            return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for updating mixin products. check if you are connected to mixin website")

    @staticmethod
    async def update_basalam_product(token: str ,product_id: int, basalam_body: dict):
        method=patch
        url=f"https://core.basalam.com/v3/products/{product_id}"
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        body= basalam_body
        
        response = requests.request(method=method, url=url, json=body, headers=headers)
        
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
        
        if response.status_code == 204:
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

    async def predict_category(title: str):
        method = get
        url = "https://categorydetection.basalam.com/category_detection/api_v1.0/predict/"
        params = {
            "title": title
        }
        headers = {
            'Accept': 'application/json'
        }
        
        response = requests.request(method=method, url=url, headers=headers, params=params)
        
        if response.status_code == 200:
            response = response.json()
            
            category_prediction = response
            return category_prediction
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid request for category prediction. check if you are connected to the category detection service")