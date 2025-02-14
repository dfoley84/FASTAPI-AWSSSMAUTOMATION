import boto3
import time
from env_utils import EnvUtils

class TriggerSSM:
    def __init__(self, parameters, region_name, document_name, Environment):
        self.parameters = parameters
        self.region_name = region_name
        self.document_name = document_name
        self.Environment = Environment
    
        if self.Environment == 'prod':
            self.client = boto3.client('sts')
            response = self.client.assume_role(
                RoleArn=EnvUtils.get_env_variable('PROD_ROLE_ARN'),
                RoleSessionName=EnvUtils.get_env_variable('ROLE_SESSION_NAME')
            )
        else:
            self.client = boto3.client('sts')
            response = self.client.assume_role(
                RoleArn=EnvUtils.get_env_variable('UAT_ROLE_ARN'),
                RoleSessionName=EnvUtils.get_env_variable('ROLE_SESSION_NAME')
            )
        credentials = response['Credentials']
        self.session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    def start_automation_execution(self):
        ssm_client = self.session.client('ssm', region_name=self.region_name)
        response = ssm_client.start_automation_execution(
            DocumentName=self.document_name,
            Parameters=self.parameters
        )
        print(response)
        execution_id = response['AutomationExecutionId']
         
        print(response)
        execution_id = response['AutomationExecutionId']
        while True:
            execution_status = ssm_client.get_automation_execution(AutomationExecutionId=execution_id)
            status  = execution_status['AutomationExecution']['AutomationExecutionStatus']
            if status in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
                break
            time.sleep(5)
        return {
                    "message": "SSM Document triggered successfully",
                    "status": status,
                    "response": execution_status,
                    "AutomationExecutionId": execution_id,
                    "ResponseMetadata": response['ResponseMetadata']
                }        
