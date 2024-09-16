from typing import Annotated
from fastapi import Depends, Request, HTTPException
from fastapi_azure_auth.exceptions import InvalidAuth
from fastapi_azure_auth.user import User
from auth.auth import azure_scheme

async def validate_is_admin_user(request: Request, user: User = Depends(azure_scheme)) -> None:
    if 'devops' not in user.roles:
        raise HTTPException(status_code=403, detail=f'User {user.name} is not a member of the DevOps Role Group')
    return None


'''
This should Check if the user is a member of the DevOps Role Group prior to Executing the Function, 
Currently not working as expected

DevOps = Annotated[User, Depends(validate_is_admin_user)] 
'''
