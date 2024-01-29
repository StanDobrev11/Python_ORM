from django.core.validators import BaseValidator


class RangeValidator(BaseValidator):
    message = "Ensure this value is greater than or equal to %(limit_value)s."

    def compare(self, a, b):
        return a < b