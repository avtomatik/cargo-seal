import datetime
import re


def clean_string(text: str, fill: str = ' ', pattern: str = r'\W') -> str:
    return fill.join(part for part in re.split(pattern, text.strip()) if part)


def parse_date(text: str) -> datetime.datetime:
    formats = [
        (r'(\D+) (\d{2})\, (\d{4})', '%b %d, %Y'),
        (r'(\D+), (\d{2})\ (\d{4})', '%b, %d %Y'),
        (r'(\d{2})\ (\D+), (\d{4})', '%d %B, %Y'),
        (r'(\d{2}) (\D+) (\d{4})', '%d %B %Y')
    ]

    for pattern, format in formats:
        match = re.search(pattern, text)
        if match:
            return datetime.datetime.strptime(match.group(), format)


def sort_and_concat(strings: list[str]) -> str:
    return '; '.join(sorted({item.title() for item in strings}))
