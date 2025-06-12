from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from configure import Config
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routes import basalam_client, mixin_client, user_products
import uvicorn
import requests

app = FastAPI()

@app.get("/basalam/client/get-user-access-token")
async def get_access_token(code: str, state: str):          #state is the random name you enter when creating client
                                                            #it's value in here is "management-test"
    if state != "management-test":
        return {"message": "please enter a valid state"}
    

    #creating request
    method="POST"
    url= "https://auth.basalam.com/oauth/token"         #AOuth2 request for getting access-token from basalam
    body={
        "grant_type" : "authorization_code",
        "client_id" : Config.ID,
        "client_secret" : Config.BASALAM_SECRET,
        "redirect_uri" : Config.REDIRECT_URI,
        "code" : f"{code}"
    }
    
    #send request
    response = requests.request(method=method, url=url, data=body)
    
    if response.status_code == 200:
        response = response.json()
        
        #stores tokens globaly
        global basalam_user_access_token
        global basalam_user_refresh_token
        basalam_user_access_token = basalam_user_access_token + " " + response["access_token"]
        basalam_user_refresh_token = basalam_user_access_token + " " + response["refresh_token"]
        
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        
        html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Basalam Connection</title>
            </head>
            <body>
                <script>
                    console.log('Basalam callback page loaded');
                    console.log('Window opener exists:', !!window.opener);
                    
                    if (window.opener) {{
                        console.log('Attempting to send message to opener');
                        const message = {{
                            access_token: "{access_token}",
                            refresh_token: "{refresh_token}"
                        }};
                        console.log('Message to send:', message);
                        
                        try {{
                            window.opener.postMessage(message, "*");  // Using "*" for testing
                            console.log('Message sent successfully');
                        }} catch (error) {{
                            console.error('Error sending message:', error);
                        }}
                        
                        // Close this window after a short delay
                        setTimeout(() => {{
                            window.close();
                        }}, 1000);
                    }} else {{
                        console.error('No window.opener found');
                    }}
                </script>
            </body>
            </html>
            """
        
        return  HTMLResponse(content=html_content, status_code=200)
    
    elif response.status_code == 500:
        return {"we have problem with basalam sever to for getting access and refresh token": {response.json()}}
    elif response.status_code == 401:
        return {"you have 401 not Authorized": f"{response.json()}"}
    elif response.status_code == 403:
        return {"you have 403 forbidden": f"{response.json()}"}
    else:
        return "try for getting access token failed. try sending a valid request for granting access token"
    
    
    # get response and store necessary data



origins = [
    "http://localhost:5173",
    "https://mixinsalamm.liara.run",  # Frontend URL
    "https://mixinsalam.liara.run",   # Backend URL
    "http://localhost:3000",
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
    
    if request.method != "OPTIONS":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
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



@app.get("/")
async def get_root():
    return "You are very welcome :)"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)

