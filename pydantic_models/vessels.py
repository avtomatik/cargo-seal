import datetime

from pydantic import BaseModel, field_validator


class VesselModel(BaseModel):
    name: str
    imo: int
    date: datetime.date

    @property
    def year_built(self) -> int:
        return self.date.year

    @property
    def folder_name(self) -> str:
        return f'imo_{self.imo}_{self.name.strip().lower().replace(" ", "_")}'

    @field_validator('imo')
    @classmethod
    def validate_imo(cls, value: int) -> int:
        if value < 1000000 or value > 9999999:
            raise ValueError('IMO number must be a 7-digit integer.')

        numbers = []
        temp = value
        for _ in range(7):
            temp, number = divmod(temp, 10)
            numbers.append(number)

        check_digit = numbers[0]
        calculated_check = sum(
            i * num for i, num in enumerate(numbers[1:], start=2)
        )

        if calculated_check % 10 != check_digit:
            raise ValueError('Not a valid IMO number.')

        return value
