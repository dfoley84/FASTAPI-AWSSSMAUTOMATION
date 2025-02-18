from fastapi import APIRouter, HTTPException, Form, Depends
from scripts.api_triggerssm import TriggerSSM
from typing import Optional
from model.baseclass import AWSEnvironmentEnum
import logging
import boto3

router = APIRouter()

@router.post("/sftp/",
             response_model=dict
)
def trigger_ssm_document(
    Environment: AWSEnvironmentEnum = Form(..., description="AWS Environment"),
    sftpclientname: str = Form(..., description="SFTP Client Username."),
    sftpclientbucket: str = Form(..., description="The name of the S3 bucket where the SFTP client Folders are stored."),
    clientkey: Optional[str] = Form(None, description="The Client Public Key to be imported -> Leave Blank if not available."),   
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
        ssm_client = boto3.client('ssm', region_name='eu-west-1')
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
            'sftpclientname': sftpclientname,
            'sftpclientbucket': sftpclientbucket,
            'clientkey': clientkey
        }        
        ssm = TriggerSSM(parameters_dict, "eu-west-1", env_selected['documentname'], env_selected)
        response = ssm.start_automation_execution()
        return response

    except Exception as e:
        logging.error(f"Error triggering SSM Document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering SSM Document: {str(e)}")
