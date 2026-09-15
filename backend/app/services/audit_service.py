import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from supabase import Client

logger = logging.getLogger(__name__)


def log_audit_event(
    client: Client,
    actor_id: Optional[str],
    actor_role: str,
    patient_id: str,
    action: str,
    access_type: str = "NORMAL",
    entity_type: str = "PATIENT",
    entity_id: Optional[str] = None,
    reason: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """
    Persists an immutable audit log record in the audit_logs table.
    Captures actor, target patient, action, access mode (NORMAL vs BREAK_GLASS),
    timestamp, entity reference, clinical reason, and metadata.
    """
    if not patient_id:
        return None

    now_utc = datetime.now(timezone.utc)
    audit_id = str(uuid.uuid4())

    # Map actor_id to doctor_id if actor is a doctor
    doctor_id = None
    if actor_role.upper() == "DOCTOR" and actor_id:
        try:
            # Check if actor_id is directly a doctor_id
            doc_chk = client.table("doctors").select("doctor_id").eq("doctor_id", actor_id).execute()
            if doc_chk.data:
                doctor_id = actor_id
            else:
                # If actor_id is auth_user_id, lookup doctor_id
                doc_auth = client.table("doctors").select("doctor_id").eq("auth_user_id", actor_id).execute()
                if doc_auth.data:
                    doctor_id = str(doc_auth.data[0]["doctor_id"])
        except Exception:
            doctor_id = None

    # Merge details into new_data if new_data is not provided
    payload_new_data = new_data or ({"metadata": details} if details else None)

    record = {
        "audit_id": audit_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "action": action.upper(),
        "entity_type": entity_type.upper(),
        "entity_id": entity_id or patient_id,
        "old_data": old_data,
        "new_data": payload_new_data,
        "reason": reason or f"{action} performed under {access_type} access",
        "access_type": access_type.upper(),
        "timestamp": now_utc.isoformat(),
    }

    try:
        res = client.table("audit_logs").insert(record).execute()
        if res.data:
            return str(res.data[0]["audit_id"])
    except Exception as e:
        logger.warning(f"Audit log persistence warning: {e}")

    return audit_id


def get_patient_audit_logs(
    client: Client,
    patient_id: str,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Retrieves audit history for a patient ordered by timestamp descending.
    """
    try:
        res = (
            client.table("audit_logs")
            .select("*")
            .eq("patient_id", patient_id)
            .order("timestamp", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        rows = res.data or []
        return {
            "patient_id": patient_id,
            "total_logs": len(rows),
            "logs": rows,
        }
    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        return {
            "patient_id": patient_id,
            "total_logs": 0,
            "logs": [],
        }
