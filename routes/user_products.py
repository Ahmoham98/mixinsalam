from fastapi import APIRouter, HTTPException, status, Depends, Form, UploadFile, File, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from dependencies import AccessTokenBearer

from database import get_session
from schema.mixin import MixinCreate, MixinAddToDatabase
from schema.basalam import BasalamCreate, BaslaamUpdate
from controllers.products import ProductController


import httpx
import mimetypes
from io import BytesIO


access_token_bearer = AccessTokenBearer()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


product_router = APIRouter()


@product_router.get("/my-mixin-products")
async def get_all_mixin_products(
    mixin_url: str,
    mixin_page: int = 1,
    mixin_token: str = Depends(access_token_bearer)
):
    result = await ProductController.get_mixin_products(url=mixin_url, mixin_token=mixin_token, mixin_page=mixin_page)
    return result

@product_router.get("/my-basalam-products/{vendor_id}")
async def get_all_basalam_products(
    vendor_id: int,
    basalam_page: int = 1,
    token: str = Depends(access_token_bearer),
):
    result = await ProductController.get_basalam_products(token=token ,vendor_id=vendor_id ,basalam_page=basalam_page)
    return result

@product_router.get("/is-equal")
async def check_if_is_equal(mixin_url: str, mixin_token: str, mixin_prodcut_id: int, basalam_token: str, basalam_product_id: int):
    result = await ProductController.is_equal(basalam_product_id=basalam_product_id, mixin_url=mixin_url, mixin_token=mixin_token, mixin_product_id=mixin_prodcut_id,)
    return {
        "data": {
            "message": "user check successfully!",
            "result": result
        }
    }

@product_router.get("/mixin/{mixin_product_id}")
async def get_mixin_product_by_product_id(
    mixin_url: str,
    mixin_product_id: int,
    mixin_token: str = Depends(access_token_bearer)
):
    result = await ProductController.get_mixin_product(mixin_url=mixin_url, mixin_product_id=mixin_product_id, mixin_token=mixin_token)
    return result

@product_router.get("/basalam/{basalam_product_id}")
async def get_basalam_product_by_product_id(
    basalam_product_id: int,
    token: str = Depends(access_token_bearer),
):
    result = await ProductController.get_basalam_product(token=token ,basalam_product_id=basalam_product_id)
    return result

@product_router.post("/create/mixin")
async def create_mixin_product(
    mixin_url: str,
    data: MixinCreate,
    mixin_token: str = Depends(access_token_bearer)
):
    result = await ProductController.create_mixin_product(url=mixin_url, mixin_token=mixin_token, mixin_body=data)
    return result

@product_router.post("/upload-product-image/{product_id}")
async def upload_product_image(
    product_id: int,
    photo: UploadFile = File(...),
    token: str = Depends(access_token_bearer)
):
    result = await ProductController.upload_product_image(token=token, product_id=product_id, photo=photo)
    return result

@product_router.post("/upload-image")
async def upload_image(
    photo: UploadFile = File(...),
    token: str = Depends(access_token_bearer)
):
    result = await ProductController.upload_image(token=token, file=photo)
    return result


@product_router.post("/sync-image")
async def sync_image(
    image_url: str = Query(...),
    token: str = Depends(access_token_bearer)
):
    try:
        #handling the url and convert it to a file
        
        image_data, content_type = await ProductController.download_image_with_retry(image_url)
        
        extension = mimetypes.guess_extension(content_type) or ".jpg"
        filename = "image" + extension
        
        file_like = BytesIO(image_data)         # convert the file to binary
        
        
        result = await ProductController.upload_image_from_bytes(           # send file to basalam endpoint
            token=token,
            file_bytes=file_like,
            filename=filename,
            content_type=content_type
        )
        return result

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@product_router.post("/create/basalam/{vendor_id}")
async def create_basalam_product(
    vendor_id: int,
    payload: BasalamCreate,                # <- This comes in as JSON
    token: str = Depends(access_token_bearer)
):
    # Convert Pydantic model to dict, exclude nulls
    body = payload.model_dump(exclude_none=True)
    result = await ProductController.create_basalam_product(token, vendor_id, body)
    return result

@product_router.put("/update/mixin/{mixin_product_id}")
async def update_mixin_product(
    mixin_url: str,
    mixin_product_id: int,
    mixin_body: MixinCreate,
    mixin_token: str = Depends(access_token_bearer)
):
    result = await ProductController.update_mixin_product(url=mixin_url, mixin_token=mixin_token, mixin_product_id=mixin_product_id, mixin_body=mixin_body)
    return result

@product_router.patch("/update/basalam/{product_id}")
async def update_basalam_product(
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    token: str = Depends(access_token_bearer),
):
    basalam_body = {
        "name": name,
        "price": price
    }
    
    result = await ProductController.update_basalam_product(token=token, product_id=product_id, basalam_body=basalam_body,)
    return result

@product_router.delete("/delete/mixin/{mixin_product_id}")
async def delete_mixin_product(
    mixin_product_id: int,
    mixin_url: str,
    mixin_token: str = Depends(access_token_bearer)
):
    result = await ProductController.delete_mixin_product(mixin_product_id=mixin_product_id ,url=mixin_url , mixin_token=mixin_token)
    return result

@product_router.get("/category-detection/")
async def get_category_prediction(
    title: str,
):
    result = await ProductController.predict_category(title=title)
    return result
