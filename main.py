import logging
import uvicorn
from fastapi import FastAPI, Security, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from ssm.router import router 
from auth.dependencies import validate_is_admin_user
logging.basicConfig(level=logging.INFO)


app = FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': '<client>',
        'scopes': 'api://<Scope>/user_impersonation',
    },
)


@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

app.include_router(router,
                   prefix="/ssmautomation",
                   tags=["SSM Document Automation"],
                   dependencies=[Depends(validate_is_admin_user)]
                )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
