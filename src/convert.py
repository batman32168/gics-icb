from src.taxonomy import Taxonomy
from src.mapping.gics2icb import mapping as gics_mapping

class Convert:

    @staticmethod
    def gics_to_icb(gics: Taxonomy):
        code =gics.code
        if len(code) >= 2:
            icb_code = gics_mapping.get(code)
            if icb_code is not None and icb_code != '':
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
            else:
                new_gics = Taxonomy(code[:-2], 'GICS', '2018')
                return Convert.gics_to_icb(new_gics)
        return None