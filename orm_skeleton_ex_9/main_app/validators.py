from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class RangeValidator(BaseValidator):

    def __init__(self, min_value, max_value, message=None):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(limit_value=max_value, message=message)

    def compare(self, a, b):
        return not (self.min_value <= a <= self.max_value)


def rating_validator(value):
    if value not in range(1, 11):
        raise ValidationError("The rating must be between 0.0 and 10.0")


def year_validator(value):
    if value not in range(1990, 2024):
        raise ValidationError("The release year must be between 1990 and 2023")
