from fastapi import APIRouter
import requests


basalam_client = APIRouter()

#Authorization header value for basalam requests
basalam_access_token = "Bearer"
basalam_refresh_token = "Bearer"


basalam_client.post("/get-access-token")
async def get_access_token(code: str, state: str):          #state is the random name you enter when creating client
                                                            #it's value in here is "management-test"
    #creating request
    method="POST"
    url= "https://auth.basalam.com/oauth/token"         #AOuth2 request for getting access-token from basalam
    headers={
        'Content-Type: application/json',
        'Accept: application/json'
    }
    body={
        "grant_type" : "authorization_code",
        "client_id" : "[client_id]",
        "client_secret" : "[client_secret]",
        "redirect_uri" : "[redirect_uri]",
        "code" : f"{code}"
    }
    #send request
    response = requests.request(method=method, url=url, headers=headers, data=body)
    
    if response.status_code == 200:
        pass
    else:
        return "try for getting access token failed. try sending a valid request for granting access token"
    # get response and store necessary data
    response = response.json()
    
    basalam_access = response['access_token']
    basalam_refresh = response['refresh_token']
    
    #assign basalam request Authorization header value globally
    global basalam_access_token
    basalam_access_token += basalam_access
    
    global basalam_refresh_token
    basalam_refresh_token += basalam_refresh

    return {"message": "you are successfully connected to your basalam account :)"}
    
    
#read user data from basalam v3/users/me
@basalam_client.get("/me")
async def get_my_basalam_data():
    #creating request
    method="GET"
    url= "https://core.basalam.com/v3/users/me"         #AOuth2 request for getting access-token from basalam
    headers={
        'Accept: application/json',
        f'Authorization: {basalam_access_token}'
    }
    response = requests.request(method=method, url=url, headers=headers)
    
    if response.status_code == 200:
        pass
    else:
        return {"message": "problem in fetch user data from basalam. request may have problem here... "}
    
    