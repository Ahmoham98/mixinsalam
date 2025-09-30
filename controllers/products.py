
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Content
from schema.mixin import MixinAddToDatabase, MixinCreate
from schema.basalam import BasalamCreate, BaslaamUpdate

from fastapi import HTTPException, status, UploadFile
import requests
import json
import httpx
import asyncio
import random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"

class ProductController:                # Need to assign real body data from schemas after testing the endpoint using inserted sample data
    def __init__(self):
        pass
    # ✅ helper: fetch one page with retry + exponential backoff
    @staticmethod
    async def _fetch_page(client: httpx.AsyncClient, url: str, headers: dict, params: dict, retries: int = 3):
        delay = 1
        for attempt in range(retries):
            try:
                resp = await client.get(url, headers=headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    print(f"⚠️ Failed page {params.get('page')}, status {resp.status_code}")
            except Exception as e:
                print(f"❌ Error fetching page {params.get('page')}: {e}")
            # exponential backoff + jitter
            print("before calling the sleep of asyncio")
            await asyncio.sleep(delay + random.uniform(0, 0.5))
            print("after calling the sleep of asyncio")
            
            delay *= 2
        return None
    # ✅ helper: fetch with batching
    @staticmethod
    async def _fetch_in_batches(client, base_url, headers, total_pages, per_batch=20):
        results = []
        for i in range(2, total_pages + 1, per_batch):  # start from page=2
            batch_pages = range(i, min(i + per_batch, total_pages + 1))
            tasks = [
                ProductController._fetch_page(client, base_url, headers, {"page": p})
                for p in batch_pages
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=False)
            results.extend([r for r in batch_results if r])
        return results

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
    # ✅ Aggregated Mixin fetch (batched parallel + retry)
    @staticmethod
    async def get_all_mixin_products(mixin_url: str, mixin_token: str, per_batch: int = 20):
        per_page = 100
        base_url = f"https://{mixin_url}/api/management/v1/products/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Api-Key {mixin_token}",
        }

        all_products = []
        async with httpx.AsyncClient(timeout=60.0) as client:
            # first request
            first = await ProductController._fetch_page(client, base_url, headers, {"page": 1})
            if not first:
                raise HTTPException(status_code=404, detail="Failed to fetch Mixin products")
            items = first.get("result") or first.get("products") or []
            all_products.extend(items)

            # detect total pages
            total_pages = first.get("total_pages")
            # fetch remaining in batches
            batch_results = await ProductController._fetch_in_batches(
                client, base_url, headers, total_pages, per_batch
            )
            for r in batch_results:
                all_products.extend(r.get("results") or r.get("products") or [])

        return {"count": len(all_products), "products": all_products}

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
    # ✅ Aggregated Basalam fetch (batched parallel + retry)
    @staticmethod
    async def get_all_basalam_products(token: str, vendor_id: int, per_batch: int = 20):
        per_page = 10
        base_url = f"https://core.basalam.com/v3/vendors/{vendor_id}/products"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        all_products = []
        async with httpx.AsyncClient(timeout=60.0) as client:
            # first request
            first = await ProductController._fetch_page(client, base_url, headers, {"page": 1})
            if not first:
                raise HTTPException(status_code=404, detail="Failed to fetch Basalam products")

            items = first.get("data") or first.get("products") or []
            all_products.extend(items)

            # detect total pages
            total_pages = first.get("total_page")

            # fetch remaining in batches
            batch_results = await ProductController._fetch_in_batches(
                client, base_url, headers, total_pages, per_batch
            )
            for r in batch_results:
                all_products.extend(r.get("data") or r.get("products") or [])

        return {"count": len(all_products), "products": all_products}

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
            
        return {
            "status_code": response.status_code,
            "response": response.json()
        }
    
    @staticmethod
    async def upload_image_from_bytes(token: str, file_bytes, filename: str, content_type: str):
        url = "https://uploadio.basalam.com/v3/files"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        files = {
        "file": (filename, file_bytes, content_type),
        "file_type": (None, "product.photo")
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, files=files, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Upload failed: {response.status_code}, {response.text}")

            return response.json()
        except Exception as e:
            raise
            
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
            return {
            "status_code": response.status_code,
            "response": response.json()
        }
    
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
    
    async def fetch_page(client: httpx.AsyncClient, url: str, params: dict):
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print (f"error fetching {url} with {params}: {e}")

    async def fetch_all_products(vendor_id, total_page, per_page, url, token):
        total_pages = (total_page + per_page - 1) // per_page
        results = []
        # limit concurrency (e.g. 20 at a time)
        semaphore = asyncio.Semaphore(20)

        async with httpx.AsyncClient() as client:
            async def fetch_with_sem(page: int):
                async with semaphore:
                    return await ProductController.fetch_page(client, url, {"page": page, "limit": per_page})
        
            tasks = [fetch_with_sem(page) for page in range(1, total_pages + 1)]
            pages = await asyncio.gather(*tasks)
        for page in pages:
            results.extand(page.get("prdoucts, []"))
        return results

    @retry(
        stop=stop_after_attempt(3),                     # try three more time
        wait=wait_exponential(multiplier=1, min=1, max=5),  # some delay between retries
        retry=retry_if_exception_type(httpx.RequestError)   # retry when network error
    )
    async def download_image_with_retry(image_url: str) -> tuple[bytes, str]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(image_url)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image")

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="URL is not an image")

        return response.content, content_type

    async def get_category_unit_type(category_id: int, token: str):
        method = get
        url = f"https://core.basalam.com/v3/categories/{category_id}"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.request(method=method, url=url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()