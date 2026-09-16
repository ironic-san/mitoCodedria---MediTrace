TERMS={"diabetes mellitus":"SNOMED:73211009","hypertension":"SNOMED:38341003","pneumonia":"SNOMED:233604007","myocardial infarction":"SNOMED:22298006"}
def terminology_code(value: str) -> str | None:
    return TERMS.get(value.lower().strip())
