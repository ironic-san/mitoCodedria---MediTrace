from .base_extractor import BaseExtractor
class ConditionExtractor(BaseExtractor):
    entity_type="CONDITION"
    def extract(self, text, **kwargs): return []
