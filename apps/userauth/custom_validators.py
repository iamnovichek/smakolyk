from django.core.exceptions import ValidationError

from datetime import datetime


def _is_too_young(birthdate):
    today_ = datetime.today()
    age = today_.year - birthdate.year - ((today_.month, today_.day)
                                          < (birthdate.month, birthdate.day))
    return age < 18


def _is_too_old(birthday):
    today_ = datetime.today()
    age = today_.year - birthday.year - ((today_.month, today_.day)
                                         < (birthday.month, birthday.day))
    return age > 90


def age_validator(birthday):
    if _is_too_young(birthday):
        raise ValidationError("You are too young, go to the school!")

    if _is_too_old(birthday):
        raise ValidationError("You are too old for this shit!")
