from django.core.exceptions import ValidationError


def letters_and_spaces_validator(value: str):
    for ch in value:
        if not ch.isalpha() and not ch.isspace():
            raise ValidationError("Name can only contain letters and spaces")
