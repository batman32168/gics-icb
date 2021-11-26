from src.mapping.taxonomy import TaxonomyMap
from src.definitions import *


TAXONOMIES ={
    "GICS_2014": gics_2014,
    "GICS_2016": gics_2016,
    "GICS_2018": gics_2018,
    "ICB_2014": icb_2021,
    "ICB_2016": icb_2021,
    "ICB_2018": icb_2021,
    "ICB_2021": icb_2021,
}

BENCHMARKS ={
    "GICS",
    "ICB"
}
YEAR ={
    "2014", "2016", "2018", "2021"
}

DEFAULT_CLASSIFICATION ="GICS"
DEFAULT_CLASSIFICATION_YEAR = '2018'

class Taxonomy:
    def __init__(self, code: str = None, benchmark: str = DEFAULT_CLASSIFICATION, year: str = DEFAULT_CLASSIFICATION_YEAR):
        """Represents a Classification code. You can instantiate GICS/ICB codes using a string representing a code.
        The string has to be a valid classification. If it's not, that is_valid method will return false.
        Note:
            that creating an empty classification will mark it as invalid but can still be used to query the definitions
            (although that object itself will not be a definition)
        Args:
         code (str): Classification code to parse. Valid codes are strings 2 to 8 characters long, with even length.
         benchmark (str): Type of classification. Possible values are GICS and ICB
         year (str): Year of the definition of the classification
        Raises:
            ValueError: When given an invalid version
        """
        self._year=year
        _definition = TAXONOMIES.get("{}_{}".format(benchmark,year))

        if not _definition:
            raise ValueError(f'Unsupported benchmark {benchmark} and/or year {year} combine. Available pairs are '
                             f'{list(TAXONOMIES.keys())}')

        self._definition = TaxonomyMap.create_recursively(_definition)

        self._code = code

        if self.is_valid:
            self._levels = [
                self._get_definition(code[:2]),
                self._get_definition(code[:4]) if len(code) >= 4 else None,
                self._get_definition(code[:6]) if len(code) >= 6 else None,
                self._get_definition(code[:8]) if len(code) == 8 else None
            ]
        else:
            self._code = None

    @property
    def definition(self):
        return self._definition

    @property
    def is_valid(self) -> bool:
        return self.code and isinstance(self.code, str) and len(self.code) >= 2 and len(self.code) <= 8 and len(
            self.code) % 2 == 0 and self._definition.get(self.code)

    @property
    def code(self):
        return self._code

    @property
    def current_level(self):
        """Gets the current level of this classification
        Returns:
            The value of the current level
        """
        return round(len(self.code)/2)

    @property
    def year(self):
        return self._year

    @property
    def first_level(self):
        """Gets the definition for the level 1
        Returns:
            Definition of the classification level. It has 3 properties: name, description and code.
            Keep in mind that only level 1 (ICB) and level 4 usually has a description.
        """
        return self.level(1)

    @property
    def second_level(self):
        """Gets the definition  level 2
        Returns:
            Definition of the classification level. It has 1 property: name
        """
        return self.level(2)

    @property
    def third_level(self):
        """Gets the definition for the level 3
        Returns:
            Definition of the classification level. It has 1 property: name.
        """
        return self.level(3)

    @property
    def fourth_sector(self):
        """Gets the definition for the level 4.
        Returns:
            Definition of the classification level. It has 3 properties: name, description and code.
        """
        return self.level(4)

    @property
    def children(self):
        """Gets all the child level elements from this classification level.
        For example, for a 1st level classification, it will return all 2nd level in that folder.
        If the classification is invalid (or empty, as with a null code), it will return all 1st level classification.
        A 4th level classification will return an empty array.
        Returns:
            List containing objects with properties code (the classification code), name (the name of this
            classification), and description (where applicable)
        """
        if self.is_valid:
            keys = filter(lambda k: k.startswith(self._code) and len(k) == len(self._code) + 2, self._definition.keys())
        else:
            keys = filter(lambda k: len(k) == 2, self._definition.keys())

        return list(map(lambda k: TaxonomyMap({
            'code': k,
            'name': self._definition[k].name,
            'description': self._definition[k].description
        }), keys))

    def _get_definition(self, code):
        definition = self._definition[code]
        definition.code = code
        return definition

    def level(self, level: int):
        """Gets the definition of the given level for this classification object.
        Args:
            level: Level of classification to get.
                Valid levels are: 1, 2, 3, 4
        Returns:
            The level of the current classification. None if no valid classification is given.
        """
        if not self.is_valid or not level or not isinstance(level,int) or level < 1 or level > 4:
            return None
        return self._levels[level - 1]



    def is_same(self, another_icb: 'ICB') -> bool:
        """Determines if this ICB is the same as the given one.
        To be considered the same both ICB must either be invalid, or be valid and with the exact same code.
        This means that they represent the same values at the same level.
        Args:
            another_icb: ICB object to compare with
        """
        return another_icb and (self.is_valid == another_icb.is_valid) and (
                self.is_valid is False or self._code == another_icb.code)

    def is_within(self, another_icb: 'ICB'):
        """Determines if this ICB is a sub-component of the given ICB. For example, ICB 101010 is within ICB 10.
        Invalid ICB do not contain any children or belong to any parent, so if any of the ICB are invalid,
        this will always be false.
        Two ICB that are the same are not considered to be within one another (10 does not contain 10).
        Args:
            another_icb: ICB object to compare with
        """
        return self.is_valid and another_icb.is_valid and self._code != another_icb.code and self._code.startswith(
            another_icb.code)

    def is_immediate_within(self, another_icb: 'ICB'):
        """Determines if this ICB is a sub-component of the given ICB at the most immediate level. For example, ICB
        1010 is immediate within ICB 10, but 101010 is not.
        Invalid ICB do not contain any children or belong to any parent, so if any of the ICB are invalid,
        this will always be false.
        Two ICB that are the same are not considered to be within one another (10 does not contain 10).
        Args:
            another_icb: ICB object to compare with
        """
        return self.is_valid and another_icb.is_valid and self._code != another_icb.code and self._code.startswith(
            another_icb.code) and len(self._code) == len(another_icb._code) + 2

    def contains(self, another_icb: 'ICB'):
        """Determines if this ICB contains the given ICB. For example, ICB 10 contains ICB 101010.
        Invalid ICB do not contain any children or belong to any parent, so if any of the ICB are invalid,
        this will always be false.
        Two ICB that are the same are not considered to be within one another (10 does not contain 10).
        Args:
            another_icb: ICB object to compare with
        """
        return another_icb.is_within(self)

    def contains_immediate(self, another_icb: 'ICB'):
        """Determines if this ICB contains the given ICB at the most immediate level. For example, ICB 10 contains
        immediate ICB 1010, but not 101010.
        Invalid ICB do not contain any children or belong to any parent, so if any of the ICB are invalid, this will
        always be false.
        Two ICB that are the same are not considered to be within one another (10 does not contain 10).
        Args:
            another_icb: ICB object to compare with
        """
        return another_icb.is_immediate_within(self)