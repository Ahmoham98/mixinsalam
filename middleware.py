from fastapi import FastAPI
from fastapi.requests import Request
import logging
import time

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware



logger = logging.getLogger('uvicorn.access')
logger.disabled = True

def register_middleware(app: FastAPI):
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173","https://mixinsalamm.liara.run"],  # Your frontend domain
        allow_credentials=False,  # Must match frontend withCredentials
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = ["*"]
    )
    
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        message = f" {request.client.host} - {request.client.port} - {request.method} - {request.url.path} - {request.state} - completed after: -- {processing_time} -- "
        print(message)
        
        return response 
