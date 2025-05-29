from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
import requests
import json
from dependencies import AccessTokenBearer
from configure import Config

access_token_bearer = AccessTokenBearer()

basalam_client = APIRouter()

basalam_user_access_token = "Bearer"
basalam_user_refresh_token = "Bearer"


post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


@basalam_client.get("/get-user-access-token")
async def get_access_token(code: str, state: str):          #state is the random name you enter when creating client
                                                            #it's value in here is "management-test"
    if state != "management-test":
        return {"message": "please enter a valid state"}
    

    #creating request
    method=post
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

@basalam_client.get("/get-client-access-token")
async def get_client_access_token():
    method=post
    url='https://auth.basalam.com/oauth/token'
    body={
        "client_id" : 1083,
        "client_secret" : Config.BASALAM_SECRET,
        "grant_type" : "client_credentials",
        "scope": "*"
    }
    response = requests.request(method=method, url=url, data=body)
    
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
        return response
    
    else:
        return {
            "message": "problem in fetch user data from basalam. request may have problem here... ",
            "status_code": response.status_code,
            "response": response.json()
        }


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