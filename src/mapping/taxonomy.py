class TaxonomyMap(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @staticmethod
    def create_recursively(data: dict) -> 'TaxonomyMap':
        data = TaxonomyMap(data)

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = TaxonomyMap.create_recursively(value)

        return data