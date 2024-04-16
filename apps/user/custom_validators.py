from django.core.exceptions import ValidationError

from datetime import datetime

from .values import ValidationMessages, ValidationValues


def is_too_young(birthdate):
    today_ = datetime.today()
    age = (
        today_.year
        - birthdate.year
        - ((today_.month, today_.day) < (birthdate.month, birthdate.day))
    )
    return age < ValidationValues.minimal_user_age


def is_too_old(birthday):
    today_ = datetime.today()
    age = (
        today_.year
        - birthday.year
        - ((today_.month, today_.day) < (birthday.month, birthday.day))
    )
    return age > ValidationValues.maximal_user_age


def age_validator(birthday):
    if is_too_young(birthday):
        raise ValidationError(ValidationMessages.too_young_validation_message)

    if is_too_old(birthday):
        raise ValidationError(ValidationMessages.too_old_validation_message)
