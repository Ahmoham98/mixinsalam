from fastapi import FastAPI
from routes import basalam_client, mixin_client, user_products


app = FastAPI()



app.include_router(basalam_client.basalam_client, prefix="/basalam/client", tags=["basalam_client"])
app.include_router(mixin_client.mixin_client, prefix="/mixin/client", tags=["mixin_client"])
app.include_router(user_products.product_router, prefix="/products", tags=["products"])



@app.get("/")
async def get_root():
    return "You are very welcome :)"