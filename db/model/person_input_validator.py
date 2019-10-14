import datetime
import re
from enum import Enum

from db.model.person import Person


class ValidationResult(Enum):
    ABSENT = 1
    VALID = 2
    INVALID = 3


class PersonInputValidator:
    """
        validators for person input data
    """
    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    @classmethod
    def validate_email(cls, **person_input):
        if 'email' in person_input:
            if cls.EMAIL_REGEX.match(person_input['email']):
                return ValidationResult.VALID
            else:
                return ValidationResult.INVALID
        else:
            return ValidationResult.ABSENT

    @classmethod
    def validate_birthday(cls, **person_input):
        if 'birthday' in person_input:
            try:
                datetime.date.fromisoformat(person_input['birthday'])
                return ValidationResult.VALID
            except ValueError:
                return ValidationResult.INVALID
        else:
            return ValidationResult.ABSENT

    @classmethod
    def has_all_properties(cls, **person_input):
        attributes = Person.all_properties()
        invalid_attributes = []
        for attribute in attributes:
            if attribute not in person_input:
                invalid_attributes.append((attribute, ValidationResult.ABSENT))
            elif attribute in person_input and not person_input[attribute]:
                invalid_attributes.append((attribute, ValidationResult.INVALID))
        return invalid_attributes
