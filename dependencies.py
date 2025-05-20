from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from utils.utilities import decode_token

post = "POST"
get = "GET"
put = "PUT"
patch = "PATCH"
delete = "DELETE"


#Base class for doing all fo the jwt checks
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        scheme= creds.scheme
        token = creds.credentials
        
        """#aioredis part for revoke an access token and logout
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token"
                        }
            )"""
        
        self.verify_token_data(token_data=token)
        
        """data = {
            "scheme": scheme,
            "token": token
        }"""
        
        return token
    
    def token_valid(self, token: str) -> bool:
        
        token_data = decode_token(token=token)
        
        if token_data is not None:
            return True 
        else :
            return False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes... ")
    
    

#child classes for checking access token and refresh token

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
            if not token_data :
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide an access token... "
                )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
            if token_data and not token_data["refresh"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide a refresh token... "
                )


class EqualityChecker:
    def __init__(self, handler, mixin_body: dict, basalam_body: dict):
        self.mixin_body = mixin_body
        self.basalam_body = basalam_body
        self.handler = handler
    
    def __call__(self):

        
        if self.handler == get:
            #Equality checker specified if user tried to get product
            
            #checks if product titles and price are the same
            if self.mixin_body['result']['name'] != self.basalam_body['data']['title']:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Base on checking we did, prodcuts in Mixin and Basalam Are not the same. Difference could be in products title, please Update the product in update section to make them both same for you... ")
            if self.mixin_body['result']['price'] != self.basalam_body['data']['price']:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Base on checking we did, prodcuts in Mixin and Basalam Are not the same. Difference could be in product price, please Update the product in update section to make them both same for you... ")
        
        if self.handler == post:
            #Equality checker specified if user tried to create product
            pass
        
        
        if self.handler == put:
            #Equality checker specified if user tried to create product
            pass





