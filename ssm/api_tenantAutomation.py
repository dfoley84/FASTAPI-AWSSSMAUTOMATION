from fastapi import APIRouter, HTTPException, Form, Depends
from scripts.api_triggerssm import TriggerSSM
from typing import Optional
from model.baseclass import AWSEnvironmentEnum, AWSRegionEnum,TenantSuperUser, TenantSuperUserName
import logging
import boto3

router = APIRouter()

@router.post("/FusionTenant/",
             response_model=dict
)
def trigger_ssm_document(
    Region: AWSRegionEnum = Form(..., description="AWS Region"),
    Environment: AWSEnvironmentEnum = Form(..., description="AWS Environment"),
    SuperAdmin: TenantSuperUser = Form(..., description=""),
    SuperUserName: TenantSuperUserName = Form(..., description=""),
    Tenantprefix: str = Form(..., description=""),
    TenantDisplayName: str = Form(..., description="")
):
    role = {
        "uat": {
            "documentname": "ssm-automation-uat-",
        },
        "prod": {
            "documentname": "ssm-automation-prod-",
        }
    }

    if Environment.value not in role:
        raise HTTPException(status_code=400, detail="Invalid environment")

    env_selected = role[Environment]

    try:
        ssm_client = boto3.client('ssm', region_name=Region)
         #Fetch the Full Document Name From the Environment
        DocName = ssm_client.list_documents(
            DocumentFilterList=[
                {
                    'key': 'Owner',
                    'value': 'Self',
                },
                {
                    'key': 'DocumentType',
                    'value': 'Automation',
                },
                {
                    'key': 'Name',
                    'value': env_selected['documentname']
                }
            ]
        )
        # Fetch parameters dynamically from SSM Document
        response = ssm_client.describe_document(
            Name=DocName['DocumentIdentifiers'][0]['Name']
        )
        parameters = response['Document']['Parameters']
        if not parameters:
            raise HTTPException(status_code=404, detail="Parameters not found")
        
        parameters_dict = {param['Name']: param.get('DefaultValue', '') for param in parameters}
        parameters_dict = {
            'SuperAdminEmail': SuperAdmin.value,
            'SuperAdminName': SuperUserName,
            'Tenantprefix': Tenantprefix, 
            'TenantDisplayName': TenantDisplayName
        }
        ssm = TriggerSSM(parameters_dict, Region, env_selected['documentname'], env_selected)
        response = ssm.start_automation_execution()
        return response

    except Exception as e:
        logging.error(f"Error triggering SSM Document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering SSM Document: {str(e)}")
