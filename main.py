from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routes import basalam_client, mixin_client, product_images, user_products
import uvicorn

app = FastAPI()

#some comment
origins = [
    "http://localhost:5173",
    "https://mixinsalamm.liara.run",  # Frontend URL
    "https://mixinsalam.liara.run",   # Backend URL
    "http://localhost:3000",
    "https://mixinsalama-reactt.liara.run",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials"
    ],
    expose_headers=["Content-Length", "X-Requested-With"],
    max_age=3600,
)

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "https://mixinsalamm.liara.run",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Content-Type, Accept, Authorization, Origin, X-Requested-With, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
    )


app.include_router(basalam_client.basalam_client, prefix="/basalam/client", tags=["basalam_client"])
app.include_router(mixin_client.mixin_client, prefix="/mixin/client", tags=["mixin_client"])
app.include_router(user_products.product_router, prefix="/products", tags=["products"])
app.include_router(product_images.image_router, prefix="/images", tags=["product images"])


@app.get("/")
async def get_root():
    return "You are very welcome :)"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)

