from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Item(BaseModel):
    AutomationExecutionId: str

class AWSRegionEnum(str, Enum):
    eu_west_1 = "eu-west-1"
    us_west_2 = "us-west-2"
    ap_southeast_2 = "ap-southeast-2"

class NewClient(str, Enum):
    yes = "yes"
    no = "no"

class AWSEnvironmentEnum(str, Enum):
    prod = "prod"
    uat = "uat"

class TenantSuperUser(str, Enum):
    NAME = "NAME@NAME.com"


class TenantSuperUserName(str, Enum):
    NAME = "NAME"
