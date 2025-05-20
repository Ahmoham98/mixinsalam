
from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.mixin import MixinAddToDatabase


class ProductController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_mixin_product(self,):
        pass
    
    async def create_basalam_product(self,):
        pass
    
    async def update_mixin_product(self,):
        pass
    
    async def update_basalam_product(self,):
        pass
    
    async def delete_products(self, mixin: bool, basalam: bool):
        pass