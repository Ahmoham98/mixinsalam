from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from configure import Config
import requests

callback_router = APIRouter()



@callback_router.get("/callback")
async def basalam_callback(code: str, state: str):
    if state != "management-test":
        return {"message": "please enter a valid state"}
    
    #creating request
    method = "post"
    url = "https://auth.basalam.com/oauth/token"         #AOuth2 request for getting access-token from basalam
    body = {
        "grant_type": "authorization_code",
        "client_id": Config.ID,
        "client_secret": Config.BASALAM_SECRET,
        "redirect_uri": Config.REDIRECT_URI,
        "code": code
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
        
        # Redirect to frontend with success
        return RedirectResponse(url="/?basalam_connected=true")
    
    elif response.status_code == 500:
        return RedirectResponse(url="/?error=basalam_server_error")
    elif response.status_code == 401:
        return RedirectResponse(url="/?error=basalam_unauthorized")
    elif response.status_code == 403:
        return RedirectResponse(url="/?error=basalam_forbidden")
    else:
        return RedirectResponse(url="/?error=basalam_token_failed")