from fastapi import APIRouter
from ssm.api_sftp import router as sftp_router 


router = APIRouter()

#Import the Module Routers
router.include_router(sftp_router)





