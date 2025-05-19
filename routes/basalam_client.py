from fastapi import APIRouter, HTTPException, status, Depends
import requests
import json
from dependencies import AccessTokenBearer

access_token_bearer = AccessTokenBearer()

basalam_client = APIRouter()

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


@basalam_client.post("/get-user-access-token")
async def get_access_token(code: str, state: str):          #state is the random name you enter when creating client
                                                            #it's value in here is "management-test"
    if state != "management-test":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are in a wrong state. make sure your state is vaild...")
    
    #creating request
    method=post
    url= "https://auth.basalam.com/oauth/token"         #AOuth2 request for getting access-token from basalam
    headers={
        'Content-Type: application/json',
        'Accept: application/json'
        
    }
    body={
        "grant_type" : "authorization_code",
        "client_id" : client_id,
        "client_secret" : client_secret,
        "redirect_uri" : redirect_uri,
        "code" : code
    }
    #send request
    response = requests.request(method=method, url=url, headers=headers, data=body)
    
    if response.status_code == 200:
        pass
    else:
        return "try for getting access token failed. try sending a valid request for granting access token"
    # get response and store necessary data
    response = response.json()
    
    basalam_access_token = response['access_token']
    basalam_refresh_token = response['refresh_token']

    data = {
        "baslam-credentials": {
            "access-token": basalam_access_token,
            "refresh-token": basalam_refresh_token
        }
    }

    return data

@basalam_client.get("/get-client-access-toke")
async def get_client_access_token():
    method=post
    url='https://auth.basalam.com/oauth/token'
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    body={
        "client_id" : client_id,
        "client_secret" : client_secret,
        "grant_type" : "client_credentials",
        "scope": "*"
    }
    response = requests.request(method=method, url=url, headers=headers, data=body)
    
    if response.status_code == 200:
        
        response = response.json()
        
        token_type = response['token_type']
        expire_time = response['expires_in']
        client_access_token = response['access_token']
    
        data = {
            "client": {
                "token_type": token_type,
                "expires_in": expire_time,
                "access_token": client_access_token
            }
        }
        return data
    else:
        raise HTTPException(status_code=404, detail="Can't send valid request for getting client access token!")

#read user data from basalam v3/users/me
@basalam_client.get("/me")
async def get_my_basalam_data(token: str = Depends(access_token_bearer)):
    
    if not token: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="make sure you provided a valid user baerer access token as a value for Authorization header")
    
    #creating request
    method=get
    url= "https://core.basalam.com/v3/users/me"         #AOuth2 request for getting access-token from basalam
    headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        
        response = response.json()
        
        user_id = response['id']
        user_hash_id = response['hash_id']
        username = response['username']
        name = response['name']
        
        vendor_id = response['vendor']['id']
        vendor_identifier = response['vendor']['identifier']
        vendor_title = response['vendor']['title']
        
        data = {
            "user": {
                "id": user_id,
                "hash_id": user_hash_id,
                "username": username,
                "name": name
            },
            "vendor": {
                "id": vendor_id,
                "identifier": vendor_identifier,
                "title": vendor_title
            }
        }
        return data
    else:
        return {"message": "problem in fetch user data from basalam. request may have problem here... "}


@basalam_client.get("/verify-my-token")
async def verify_token(token: str = Depends(access_token_bearer)):
    
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="please make sure you provided a valid user bearer access token as a value for Authorization header")
    
    method = get
    url = "https://auth.basalam.com/whoami"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        raise HTTPException(status_code=200, detail="Your token is valid")
    else:
        raise HTTPException(status_code=404, detail="your token is not valid")