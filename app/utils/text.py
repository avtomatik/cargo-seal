import re
from typing import Optional

from app.constants import CYRILLIC_TO_LATIN


def clean_string(text: str, fill: str = ' ', pattern: str = r'\W') -> str:
    return fill.join(part for part in re.split(pattern, text.strip()) if part)


def transliterate_to_latin(
    word: str, mapping: dict[str, str] = CYRILLIC_TO_LATIN
) -> str:
    return ''.join(mapping.get(char.lower(), char) for char in word)


def regex_trim(value: str, pattern: str, group_name: str) -> Optional[str]:
    """Generic function to apply regex and extract the named group."""
    if isinstance(value, str):
        match = re.search(pattern, value)
        if match:
            return match.group(group_name)
    return value


def regex_trim_country(value: str) -> Optional[str]:
    pattern = (
        r'One Or \w+\s+Safe\s+Port(?:\s+S|s)?\s+'
        r'(?P<country>.+)$'
    )
    return regex_trim(value, pattern, 'country')


def regex_trim_entity(value: str) -> Optional[str]:
    return regex_trim(value, r'To The Order Of (?P<entity>.*)', 'entity')


def regex_trim_for_orders(value: str) -> Optional[str]:
    return regex_trim(value, r'(?P<country>.*) For Orders', 'country')
