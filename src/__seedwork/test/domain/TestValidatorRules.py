import unittest

from src.__seedwork.domain.exceptions import ValidationException
from src.__seedwork.domain.validators import ValidatorRules


class MyTestCase(unittest.TestCase):
    invalid_data = [
        {'value': None, 'prop': 'prop'},
        {'value': '', 'prop': 'prop'},
    ]

    def teste_constructor(self):
        validator = ValidatorRules.values('some value', 'prop')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.prop, 'prop')

    def test_required_rule(self):
        self.assertIsInstance(
            ValidatorRules.values('some value', 'prop').required(),
            ValidatorRules
        )

    def test_required_rule_throw_when_passed_values(self):
        for data in self.invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.values(**data).required(),
                    ValidatorRules
                )
            self.assertEqual('The prop is required', assert_error.exception.args[0])
