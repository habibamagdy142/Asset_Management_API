from pydantic import BaseModel,Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class AssetType(str, Enum):
    domain = "domain"
    subdomain = "subdomain"
    ip_address = "ip_address"
    service = "service"
    certificate = "certificate"
    technology = "technology"


class AssetStatus(str, Enum):
    active = "active"
    stale = "stale"
    archived = "archived"

class AssetCreate(BaseModel):

    type: AssetType
    value: str
    status: AssetStatus = AssetStatus.active
    source: str
    tags: List[str] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)



class AssetUpdate(BaseModel):

    status: Optional[AssetStatus] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict] = None



class AssetResponse(AssetCreate):

    id: str
    first_seen: datetime
    last_seen: datetime


    class Config:
        from_attributes = True