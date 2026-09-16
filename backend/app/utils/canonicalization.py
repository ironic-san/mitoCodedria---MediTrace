import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Tuple


CANONICAL_FIELDS = (
    "event_type",
    "event_value",
    "severity",
    "reaction",
    "event_date",
    "version",
    "status",
)


def _normalize_string(value: Any) -> str:
    """Backend-defined normalization for canonical string values."""
    if value is None:
        return ""
    return str(value).strip()


def _normalize_event_date(value: Any) -> str:
    """
    Normalize an event date to UTC ISO-8601 with a trailing Z.

    Date-only values are interpreted as midnight UTC.
    """
    raw = _normalize_string(value)

    if not raw:
        return ""

    # Date-only value: YYYY-MM-DD
    if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
        return f"{raw}T00:00:00Z"

    normalized = raw.replace("Z", "+00:00")

    try:
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        return dt.isoformat().replace("+00:00", "Z")
    except ValueError:
        # Keep deterministic behavior for an already backend-normalized value.
        return raw


def build_canonical_event(
    *,
    event_type: Any,
    event_value: Any,
    severity: Any,
    reaction: Any,
    event_date: Any,
    version: Any,
    status: Any,
) -> Dict[str, Any]:
    """
    Build the exact seven-field canonical representation used by MediTrace.

    The canonical fields are:
        event_type
        event_value
        severity
        reaction
        event_date
        version
        status
    """
    return {
        "event_type": _normalize_string(event_type).upper(),
        "event_value": _normalize_string(event_value),
        "severity": _normalize_string(severity).upper(),
        "reaction": _normalize_string(reaction),
        "event_date": _normalize_event_date(event_date),
        "version": int(version),
        "status": _normalize_string(status).upper(),
    }


def canonicalize_medical_event(event: Dict[str, Any]) -> str:
    """
    Serialize an already prepared canonical event deterministically.

    Exactly seven fields are included. Keys are alphabetically sorted,
    JSON is compact, and UTF-8 is used for hashing.
    """
    missing = [field for field in CANONICAL_FIELDS if field not in event]
    if missing:
        raise ValueError(
            f"Canonical event is missing required fields: {', '.join(missing)}"
        )

    canonical = {
        field: event[field]
        for field in CANONICAL_FIELDS
    }

    return json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def hash_canonical_string(canonical_str: str) -> str:
    """Compute the SHA-256 lowercase hexadecimal digest."""
    return hashlib.sha256(
        canonical_str.encode("utf-8")
    ).hexdigest()


def canonicalize_and_hash_event(
    event: Dict[str, Any],
) -> Tuple[str, str]:
    """Return (canonical_json, sha256_hex_digest)."""
    canonical_str = canonicalize_medical_event(event)
    return canonical_str, hash_canonical_string(canonical_str)
