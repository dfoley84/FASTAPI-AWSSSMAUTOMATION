from fastapi import APIRouter,HTTPException, Form
from pydantic import BaseModel
from scripts.api_triggerssm import TriggerSSM
from typing import Optional
from enum import Enum
import logging


router = APIRouter()
class Item(BaseModel):
    AutomationExecutionId: str

class AWSEnvironmentEnum(str, Enum):
    prod = "prod"
    uat = "uat"

class SSMDocumentParams(BaseModel):
    sftpclientname: str
    sftpclientbucket: str
    clientkey: Optional[str] = None
 

@router.post("/sftp/",
             response_model=Item,
             responses={200: {"model": Item}}
)
def trigger_ssm_document(
    Environment: AWSEnvironmentEnum = Form(..., description="AWS Environment"),
    sftpclientname: str = Form(..., description="SFTP Client Username."),
    sftpclientbucket: str = Form(..., description="The name of the S3 bucket where the SFTP client Folders are stored."),
    clientkey: Optional[str] = Form(None, description="The Client Public Key to be imported -> Leave Blank if not available."),   
):
    role = {
        "prod": {
            "documentname" : "",
            "sftprolearn": "",
            "sftpserverid": "",
            "privatekeybucketname": "",
            "sftpbucketname": ""
        },
        "uat": {
            "documentname" : "",
            "sftprolearn": "",
            "sftpserverid": "",
            "privatekeybucketname": "",
            "sftpbucketname": ""
        }
    }
    
    env_selected = role[Environment.value]
    try:
        parameters = {
            'sftpclientname': [sftpclientname],
            'sftpclientbucket': [sftpclientbucket],
            'sftprolearn': [env_selected['sftprolearn']],
            'sftpserverid': [env_selected['sftpserverid']],
            'privatekeybucketname': [env_selected['privatekeybucketname']],
            'sftpbucketname': [env_selected['sftpbucketname']]
        }
        if clientkey:
            parameters['clientkey'] = [clientkey]

        ssm = TriggerSSM(parameters, "eu-west-1", env_selected['documentname'])
        response = ssm.start_automation_execution()
        return response
      
    except Exception as e:
        logging.error(f"Error triggering SSM Document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering SSM Document: {str(e)}")
