from typing import List
from pydantic import BaseModel
import uuid

class MixinCreate(BaseModel):
    name: str
    main_category: int
    description: str | None
    analysis: str | None
    english_name: str | None
    other_categories: List[int] | None
    brand: int | None 
    is_digital: bool = False
    price: int | None
    compare_at_price: int | None
    special_offer: bool = False
    special_offer_end: str | None
    length: int | None
    width: int | None
    height: int | None
    weight: int | None
    barcode: str | None
    stock_type : str | None = "unlimited"
    stock: int | None
    max_order_quantity: int | None
    guarantee: str | None
    product_identifier: str | None
    old_path: str | None
    old_slug: str | None
    has_variants: bool = False
    available: bool = True
    seo_title: str | None
    seo_description: str | None
    extra_fields: List[str] | None
    
class MixinAddToDatabase:
    uid: uuid.UUID
    mixin_id: int
    name: str
    price: int
    description: str | None


class ProductIDs(BaseModel):
    ids: List[int]