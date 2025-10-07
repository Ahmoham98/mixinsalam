from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import AccessTokenBearer
from schema.google_sheet.comments import Comment
from controllers.google_sheet.google_sheet_users import UsersOperationController
from controllers.google_sheet.google_sheet_comments import CommentsController
from schema.google_sheet.google_sheet_users import Users

comments_router = APIRouter()
access_token_bearer = AccessTokenBearer()


# Helper to get current user id from token (stub, replace with real logic)
async def get_current_user(token: str = Depends(access_token_bearer)):
    users = await UsersOperationController.get_all_users_from_google_sheet()
    for user in users:
        if user.get("mixin_access_token") == token or user.get("basalam_access_token") == token:
            return user
    raise HTTPException(status_code=401, detail="User not found for provided token")

# Helper function to check if the current user is admin. if yes True else False
async def is_admin(token: str = Depends(access_token_bearer)):
    # TODO: decode token and check user role
    user = await get_current_user(token)
    #checkes admin privilage
    if user["role"] == "admin":
        return True
    else:
        return False

# creates new comment when user sends ticket
@comments_router.post("/")
async def create_comment(comment: Comment, user: Users = Depends(get_current_user)):
    return await CommentsController.create_comment(comment, user)

# gets new comments only admin privilages
@comments_router.get("/")
async def get_all_comments(check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await CommentsController.get_all_comments()
    else:
        return "you don't have enough privilages"

# get comment by id
@comments_router.get("/{comment_id}")
async def get_comment_by_id (comment_id: int, check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await CommentsController.get_comment_by_id(comment_id)
    else:
        return "you don't have enough privilages"

# updates comment only admin privilages
@comments_router.put("/{comment_id}")
async def update_comment(comment_id: int, comment: Comment, check_admin: bool = Depends(is_admin), user: Users = Depends(get_current_user)):
    if check_admin == True:
        return await CommentsController.update_comment(comment_id, comment, user)
    else:
        return "you don't have enough privilages"
    
# delete comment only admin privilages
@comments_router.delete("/{comment_id}")
async def delete_comment(comment_id: int, check_admin: Users = Depends(is_admin)):
    if check_admin == True:
        return await CommentsController.delete_comment(comment_id)
    else:
        return "you don't have enough privilages"
    



