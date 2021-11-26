from src.taxonomy import Taxonomy
from src.mapping.gics2icb import mapping as gics_mapping

class Convert:

    @staticmethod
    def gcis_to_icb(gics: Taxonomy):
        code =gics.code
        icb_code = gics_mapping.get(code)
        if icb_code is not None:
            icb_classification = Taxonomy(icb_code,'ICB',gics.year)
            description ="";
            current_level = icb_classification.current_level
            definition =  icb_classification.level(current_level)
            if current_level ==1 or current_level ==4:
                description = definition['description']
            return {
                'code': icb_classification.code,
                'name': definition['name'],
                'description': description
            }
        return None