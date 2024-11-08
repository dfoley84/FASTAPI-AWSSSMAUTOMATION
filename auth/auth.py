from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from env_utils import EnvUtils

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=EnvUtils.get_env_variable('AZURE_CLIENT_ID'),
    tenant_id=EnvUtils.get_env_variable('AZURE_TENANT_ID'),
    scopes={f'api://{EnvUtils.get_env_variable('AZURE_TENANT_SCOPE')}/user_impersonation': 'user_impersonation'},
    allow_guest_users=False
)
