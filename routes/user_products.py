from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
import requests
import json

from database import get_session
from schema.mixin import MixinCreate, MixinAddToDatabase
from schema.basalam import BasalamCreate, BaslaamUpdate
from controllers.products import ProductController


post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


product_router = APIRouter()


@product_router.get("/my-mixin-products")
async def get_all_mixin_products(mixin_url: str, mixin_token: str, mixin_page: int = 1):
    result = await ProductController.get_mixin_products(url=mixin_url, mixin_token=mixin_token, mixin_page=mixin_page)
    return result

@product_router.get("/my-basalam-products")
async def get_all_basalam_products(basalam_page: int = 1):
    result = await ProductController.get_basalam_products(basalam_page=basalam_page)
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
    mixin_token: str,
    mixin_product_id: int,
):
    result = await ProductController.get_mixin_product(mixin_url=mixin_url, mixin_product_id=mixin_product_id, mixin_token=mixin_token)
    return result

@product_router.get("/basalam/{basalam_product_id}")
async def get_basalam_product_by_product_id(
    basalam_product_id: int,
):
    result = await ProductController.get_basalam_product(basalam_product_id=basalam_product_id)
    return result

@product_router.post("/mixin")
async def create_mixin_product(
    *,
    session: AsyncSession = Depends(get_session),
    mixin_url: str,
    mixin_token: str,
    data: MixinCreate,
):
    result = await ProductController.create_mixin_product(url=mixin_url, mixin_token=mixin_token, mixin_body=data)
    return result

@product_router.post("/basalam/{vendor_id}")
async def create_basalam_product(
    vendor_id: int,
    data: BasalamCreate,
):
    result = await ProductController.create_basalam_product(vendor_id=vendor_id, basalam_body=data)
    return result

@product_router.put("/mixin/{mixin_product_id}")
async def update_mixin_product(mixin_url: str, mixin_token: str, mixin_product_id: int, mixin_body: MixinCreate):
    result = await ProductController.update_mixin_product(url=mixin_url, mixin_token=mixin_token, mixin_product_id=mixin_product_id, mixin_body=mixin_body)
    return result

@product_router.put("/basalam/{vendor_id}")
async def update_basalam_product(vendor_id: int, basalam_body: BaslaamUpdate):
    result = await ProductController.update_basalam_product(vendor_id=vendor_id, basalam_body=basalam_body)
    return result

@product_router.delete("/")
async def delete_product(mixin: bool, basalam: bool):
    if mixin == True and basalam == True:
        result = await ProductController.delete_mixin_product()
        return {"message": "sorry, we don't have access to delete product from basalam from here! you have to delete it in basalam site itself :)"}
    if mixin == True and basalam == False:
        result = await ProductController.delete_mixin_product()
        return result
    if mixin == False and basalam == True:
        return {"message": "sorry, we don't have access to delete product from basalam from here! you have to delete it in basalam site itself :)"}
    else:
        pass