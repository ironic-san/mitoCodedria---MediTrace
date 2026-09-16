ABBREVIATIONS={"t2dm":"Type 2 Diabetes Mellitus","dm":"Diabetes Mellitus","htn":"Hypertension","mi":"Myocardial Infarction","pci":"Percutaneous Coronary Intervention","bid":"twice daily","od":"once daily","tid":"three times daily","prn":"as needed","po":"oral","iv":"intravenous","im":"intramuscular"}
OCR_VARIANTS={"penicillln":"Penicillin","pneurnonia":"pneumonia","lg":"1 g"}
def normalize_abbreviation(value: str) -> str:
    clean=value.strip()
    return OCR_VARIANTS.get(clean.lower(), ABBREVIATIONS.get(clean.lower(), value))
