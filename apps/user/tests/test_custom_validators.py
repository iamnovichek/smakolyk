from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.user.custom_validators import age_validator, is_too_old, is_too_young
from apps.user.values import ValidationValues


class AgeValidatorTests(TestCase):
    def setUp(self):
        self.today = datetime.today()
        self.underage_date = self.today - relativedelta(
            years=ValidationValues.minimal_user_age - 1
        )
        self.overage_date = self.today - relativedelta(
            years=ValidationValues.maximal_user_age + 1
        )
        self.valid_age_date = self.today - relativedelta(
            years=ValidationValues.minimal_user_age
        )

    def test_is_too_young(self):
        """Test that is_too_young correctly identifies underage users."""
        self.assertTrue(is_too_young(self.underage_date.date()))
        self.assertFalse(is_too_young(self.valid_age_date.date()))

    def test_is_too_old(self):
        """Test that is_too_old correctly identifies users who are too old."""
        self.assertTrue(is_too_old(self.overage_date.date()))
        self.assertFalse(is_too_old(self.valid_age_date.date()))

    def test_age_validator_valid(self):
        """Test that age_validator passes with a valid age."""
        try:
            age_validator(self.valid_age_date.date())
        except ValidationError:
            self.fail("ValidationError raised with valid age.")

    def test_age_validator_too_young(self):
        """Test that age_validator raises an error for being too young."""
        with self.assertRaises(ValidationError):
            age_validator(self.underage_date.date())

    def test_age_validator_too_old(self):
        """Test that age_validator raises an error for being too old."""
        with self.assertRaises(ValidationError):
            age_validator(self.overage_date.date())
