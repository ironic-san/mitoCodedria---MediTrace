import hashlib
import json
import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def canonicalize_medical_event(event: Dict[str, Any]) -> str:
    """
    Produce a deterministic, whitespace-normalized, sorted JSON canonical representation
    of a medical event for cryptographic hashing (SHA-256).

    Fields included in canonical hash:
    - event_id (lowercased UUID)
    - patient_id (lowercased UUID)
    - event_type (uppercase trimmed)
    - event_date (ISO date string / trimmed)
    - title (trimmed)
    - description (trimmed, empty string if None)
    - severity (uppercase trimmed, empty string if None)
    - is_critical (boolean)
    - version (integer)
    """
    event_id = str(event.get("event_id", "")).strip().lower()
    patient_id = str(event.get("patient_id", "")).strip().lower()
    event_type = str(event.get("event_type", "")).strip().upper()
    event_date = str(event.get("event_date", "")).strip()
    title = str(event.get("title", "")).strip()

    desc_raw = event.get("description")
    description = str(desc_raw).strip() if desc_raw is not None else ""

    sev_raw = event.get("severity")
    severity = str(sev_raw).strip().upper() if sev_raw is not None else ""

    is_critical = bool(event.get("is_critical", False))
    version = int(event.get("version", 1))

    canonical_dict = {
        "description": description,
        "event_date": event_date,
        "event_id": event_id,
        "event_type": event_type,
        "is_critical": is_critical,
        "patient_id": patient_id,
        "severity": severity,
        "title": title,
        "version": version,
    }

    # Deterministic JSON serialization: keys sorted, compact separators
    return json.dumps(canonical_dict, sort_keys=True, separators=(",", ":"))


def hash_canonical_string(canonical_str: str) -> str:
    """Computes standard SHA-256 hex digest of a canonical UTF-8 string."""
    return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()


def canonicalize_and_hash_event(event: Dict[str, Any]) -> Tuple[str, str]:
    """Returns a tuple of (canonical_json_string, sha256_hex_hash)."""
    canonical_str = canonicalize_medical_event(event)
    return canonical_str, hash_canonical_string(canonical_str)
