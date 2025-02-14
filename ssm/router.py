from fastapi import APIRouter
from ssm.api_sftp import router as sftp_router 
from ssm.api_dtcc   import router as dtcc_router
from ssm.api_tenantAutomation import router as tenant_router

router = APIRouter()

#Import the Module Routers
router.include_router(sftp_router)
router.include_router(dtcc_router)
router.include_router(tenant_router)  





