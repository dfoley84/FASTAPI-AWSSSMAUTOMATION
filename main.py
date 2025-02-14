import uvicorn
import sys
import logging
from fastapi import FastAPI, Request, Security, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from auth.dependencies import validate_is_admin_user
from ssm.router import router 
from env_utils import EnvUtils



sys.path.append("/code/app")

logging.basicConfig(level=logging.INFO)
app = FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': EnvUtils.get_env_variable('AZURE_CLIENT_ID'),
        'scopes': f"api://{EnvUtils.get_env_variable('Azure_CLIENT_SCOPE')}/user_impersonation",
    },
)

origins = [

    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IPFilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_ip: str):
        super().__init__(app)
        self.allowed_ip = allowed_ip
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        logging.info(f"Client IP: {client_ip}")
        if client_ip != self.allowed_ip:
            return JSONResponse(status_code=403, content={"detail": "Forbidden"})
        response = await call_next(request)
        return response
app.add_middleware(IPFilterMiddleware, allowed_ip='127.0.0.1')

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy"}

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

app.include_router(router,
                   prefix="/ssmautomation",
                   tags=["SSM Document Automation"],
                   dependencies=[Depends(validate_is_admin_user)]
                )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)