UNITS={"milligrams":"mg","milligram":"mg","grams":"g","gram":"g","micrograms":"mcg","ml":"mL","milliliters":"mL","liters":"L","mm hg":"mmHg","millimeters of mercury":"mmHg","beats/min":"bpm"}
def normalize_unit(value: str) -> str:
    return UNITS.get(value.strip().lower(), value.strip())
