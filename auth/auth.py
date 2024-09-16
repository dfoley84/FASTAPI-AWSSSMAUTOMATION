from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id="<app_client_id>",
    tenant_id="<tenant_id>",
    scopes={'api://<scope>/user_impersonation': 'user_impersonation'},
    allow_guest_users=False
)
