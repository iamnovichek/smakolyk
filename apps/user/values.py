from dataclasses import dataclass


@dataclass
class ValidationValues:
    username_min_length: int = 2
    username_max_length: int = 30
    first_name_min_length: int = 2
    first_name_max_length: int = 30
    last_name_min_length: int = 2
    last_name_max_length: int = 30
    phone_max_length: int = 30
    default_photo_size: tuple[int, int] = (200, 200)
    minimal_user_age: int = 18
    maximal_user_age: int = 90


@dataclass
class ValidationMessages:
    email_not_provided_validation_message: str = "Email is required!"
    password_not_provided_validation_message: str = "Password is required!"
    username_validation_message: str = "Username should contail at least 2 characters!"
    first_name_validation_message: str = (
        "First name should contail at least 2 characters!"
    )
    last_name_validation_message: str = (
        "Last name should contail at least 2 characters!"
    )
    too_young_validation_message: str = "You are too young, go to the school!"
    too_old_validation_message: str = "You are too old for this shit!"
    clean_username_validation_message: str = "Current username is already taken!"
    clean_phone_validation_message: str = "Current phone number is already taken!"
    clean_email_validation_message: str = "Current email is already taken!"
    clean_password_validation_message: str = "Password does not match!"
    clean_birthday_validation_message: str = "Enter a valid date!"
    invalid_login_form_message: str = "Invalid value/es! Try again or sign up!"
