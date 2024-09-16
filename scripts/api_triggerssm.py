import boto3
import time

class TriggerSSM:
    def __init__(self, parameters, region_name, document_name):
        self.parameters = parameters
        self.region_name = region_name
        self.document_name = document_name

    def start_automation_execution(self):
        ssm_client = boto3.client('ssm', region_name=self.region_name)
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
