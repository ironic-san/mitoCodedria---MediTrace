class BaseExtractor:
    entity_type = None
    def extract(self, text, **kwargs):
        raise NotImplementedError
