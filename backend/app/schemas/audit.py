from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AuditLogItem(BaseModel):
    audit_id: str
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    actor_id: Optional[str] = None
    actor_role: Optional[str] = "SYSTEM"
    action: str
    entity_type: Optional[str] = "UNKNOWN"
    entity_id: Optional[str] = None
    access_type: Optional[str] = "NORMAL"
    reason: Optional[str] = None
    timestamp: str
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    details: Optional[Dict[str, Any]] = None


class AuditHistoryResponse(BaseModel):
    patient_id: str
    total_logs: int
    logs: List[AuditLogItem] = Field(default_factory=list)
