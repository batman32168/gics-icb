from icb.definitions import d_20210101
from icb.map import Map

DEFINITIONS = {
    "20210101": d_20210101
}

DEFAULT_VERSION = '20210101'

class ICB:

    def __init__(self, code: str = None, version: str = DEFAULT_VERSION):
        """Represents a ICB code. You can instantiate ICB codes using a string representing a code.
        The string has to be a valid ICB. If it's not, that is_valid method will return false.
        Note:
            that creating an empty ICB will mark it as invalid but can still be used to query the definitions
            (although that object itself will not be a definition)
        Args:
         code (str): ICB code to parse. Valid ICB codes are strings 2 to 8 characters long, with even length.
         version (str):
        Raises:
            ValueError: When given an invalid version
        """
        self._definition_version = version
        _definition = DEFINITIONS.get(self._definition_version)

        if not _definition:
            raise ValueError(f'Unsupported ICB version: {version}. Available versions are {list(DEFINITIONS.keys())}')

        self._definition = Map.create_recursively(_definition)

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
    def industry(self):
        """Gets the definition for the sector of this ICB object (ICB level 1)
        Returns:
            Definition of the ICB level. It has 3 properties: name, description and code.
            Keep in mind that only level 1 and level 4 usually has a description.
        """
        return self.level(1)

    @property
    def super_sector(self):
        """Gets the definition for the industry group of this ICB object (ICB level 2)
        Returns:
            Definition of the ICB level. It has 3 properties: name, description and code.
            Keep in mind that only level 1 and level 4 usually has a description.
        """
        return self.level(2)

    @property
    def sector(self):
        """Gets the definition for the industry of this ICB object (ICB level 3)
        Returns:
            Definition of the ICB level. It has 3 properties: name, description and code.
            Keep in mind that only level 1 and level 4 usually has a description.
        """
        return self.level(3)

    @property
    def sub_sector(self):
        """Gets the definition for the sub-industry of this ICB object (ICB level 4)
        Returns:
            Definition of the ICB level. It has 3 properties: name, description and code.
            Keep in mind that only level 1 and level 4 usually has a description.
        """
        return self.level(4)

    @property
    def children(self):
        """Gets all the child level elements from this ICB level.
        For example, for a Industry level ICB, it will return all Supersector in that Industry.
        If the ICB is invalid (or empty, as with a null code), it will return all Industry.
        A Subsector level ICB will return an empty array.
        Returns:
            List containing objects with properties code (the ICB code), name (the name of this ICB),
            and description (where applicable)
        """
        if self.is_valid:
            keys = filter(lambda k: k.startswith(self._code) and len(k) == len(self._code) + 2, self._definition.keys())
        else:
            keys = filter(lambda k: len(k) == 2, self._definition.keys())

        return list(map(lambda k: Map({
            'code': k,
            'name': self._definition[k].name,
            'description': self._definition[k].description
        }), keys))

    def _get_definition(self, icb_code):
        definition = self._definition[icb_code]
        definition.code = icb_code

        return definition

    def level(self, icb_level: int):
        """Gets the definition of the given level for this ICB object.
        Args:
            icb_level: Level of ICB to get.
                Valid levels are: 1 (Industry), 2 (Supersector), 3 (Sector), 4 (Subsector)
        Returns:
        """
        if not self.is_valid or not icb_level or not isinstance(icb_level,
                                                                 int) or icb_level < 1 or icb_level > 4:
            return None

        return self._levels[icb_level - 1]

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