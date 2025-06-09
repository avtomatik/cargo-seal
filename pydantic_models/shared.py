from enum import Enum


class Surveyor(Enum):

    NONE = 'Unknown'
    AAA_AA = 'Aaaaaa Aaaaaaa Aaa AAA'
    AAAA_AA = 'AAA A.A.'

    @classmethod
    def parse(cls, value: str, default: 'Surveyor' = None) -> 'Surveyor':
        if default is None:
            default = cls.AAAA_AA

        if not value:
            return default

        val = value.strip().lower()

        if 'aaa' in val:
            return cls.AAA_AA
        if 'aaaaaaa' in val:
            return cls.AAA_AA

        return default
