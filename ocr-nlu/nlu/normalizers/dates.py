from datetime import datetime
import re
FORMATS=("%d/%m/%Y","%d-%m-%Y","%Y-%m-%d","%B %d %Y","%d %B %Y","%b %d %Y","%d %b %Y","%d-%b-%Y")
def normalize_date(value: str) -> str | None:
    v=re.sub(r"\s+", " ", value.strip())
    for fmt in FORMATS:
        try: return datetime.strptime(v,fmt).date().isoformat()
        except ValueError: pass
    return None
