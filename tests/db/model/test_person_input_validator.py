import pytest

from db.model.person_input_validator import PersonInputValidator, ValidationResult


class TestPersonInputValidator:

    @pytest.mark.parametrize("input_dict,expected_validation_result",
                             [({'email': 'nicole@nicole.com'}, ValidationResult.VALID),
                              ({'email': 'nicole@com'}, ValidationResult.INVALID),
                              ({}, ValidationResult.ABSENT)
                              ])
    def test_email_validation(self, input_dict, expected_validation_result):
        validation_result = PersonInputValidator.validate_email(**input_dict)
        assert validation_result == expected_validation_result

    @pytest.mark.parametrize("input_dict,expected_validation_result",
                             [({'birthday': '2019-10-12'}, ValidationResult.VALID),
                              ({'birthday': '10-10-2019'}, ValidationResult.INVALID),
                              ({}, ValidationResult.ABSENT)
                              ])
    def test_birthday_validation(self, input_dict, expected_validation_result):
        validation_result = PersonInputValidator.validate_birthday(**input_dict)
        assert validation_result == expected_validation_result

    @pytest.mark.parametrize("input_dict,absent_properties_count,invalid_property_count",
                             [({'email': 'nicole@nicole.com'}, 5, 0),
                              ({'email': 'nicole@nicole.com', 'first_name': ''}, 4, 1),
                              ({}, 6, 0)])
    def test_properties_validation(self, input_dict, absent_properties_count, invalid_property_count):
        validation_result = PersonInputValidator.has_all_properties(**input_dict)
        absent_count = 0
        invalid_count = 0
        for result in validation_result:
            if result[1] is ValidationResult.ABSENT:
                absent_count = absent_count + 1
            elif result[1] is ValidationResult.INVALID:
                invalid_count = invalid_count + 1
        assert absent_count == absent_properties_count
        assert invalid_count == invalid_property_count
