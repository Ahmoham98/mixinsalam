from typing import List, Optional
from pydantic import BaseModel, Field


class PropertyVariant(BaseModel):
    value: str
    property: str



class WholeSalePrice(BaseModel):
    price: int = Field(ge=999, le=10000000000)
    min_quantity: int = Field(ge=1)

class ProductAttributes(BaseModel):
    attribute_id: int 
    value: int | None
    selected_values: List[int] | None

class ProductVariants(BaseModel):
    price: int
    stock: int
    sku : str | None     # This is actually a Enum type that need to be fixed in future
    properties: List[PropertyVariant]
    

class ProductShipingData(BaseModel):
    illegal_for_iran: bool
    illegal_for_same_city: bool


class ProductDimentionSchema(BaseModel):
    height: int
    length: int
    width: int


class BasalamCreate(BaseModel):
    name: str  #Required
    photo: int  #Required
    category_id: int    #Required
    status: int  #Required  
    preparation_days: int   #Required
    weight: int   #Required
    package_weight: int   #Required
    primary_price: int   #Required
    stock: int   #Required
    photos: List[int] | None 
    video: str | None   
    brief: str | None  
    description: str | None  
    order: str | None  
    keywords: List[str] | None
    shipping_city_ids: List[int] | None 
    shipping_method_ids: List[int] | None 
    wholesale_prices: List[WholeSalePrice] | None
    product_attribute: List[ProductAttributes] | None
    virtual: str | None   
    variants: List[ProductVariants] | None
    shipping_data: List[ProductShipingData] | None
    unit_quantity: str | None 
    unit_type: str | None  
    sku: str | None  
    packaging_dimensions: List[ProductDimentionSchema] | None
    is_wholesale: bool | None

class UpdateVariants:
    id: int
    price: int | None  #This is actually an Enum or obj
    stock: str | None  #This is actually an Enum or obj

class BasalamUpdateInfo:
    id: int
    name: str | None
    price: int | None
    order: str | None   #This is actually an Enum or obj
    stock: str | None   #This is actually an Enum or obj
    status: str | None  #This is actually an Enum or obj
    preparation_days: str | None   #This is actually an Enum or obj
    variants: UpdateVariants | None
    product_attribute: ProductAttributes | None
    shipping_data: ProductShipingData | None 


class BaslaamUpdate(BaseModel):
    data: BasalamUpdateInfo
    
    
    class Config:
        arbitrary_types_allowed=True