from fastapi import APIRouter
import requests


basalam_user = APIRouter()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


@basalam_user.get("/bassalam/me")
async def get_current_user():
    method=get
    url="https://core.basalam.com/v3/users/me"
    headers={
        'Accept': 'application/json'
    }
    
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()