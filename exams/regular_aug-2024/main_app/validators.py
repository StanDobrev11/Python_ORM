from django.core.exceptions import ValidationError


def phone_number_validator(value):
    """ must contain only digits """
    if not value.isdigit():
        raise ValidationError('Only digits allowed')
