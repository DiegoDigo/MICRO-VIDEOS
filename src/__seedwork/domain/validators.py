import abc
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Generic, TypeVar

from rest_framework.serializers import Serializer

from src.__seedwork.domain.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == '':
            raise ValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if not isinstance(self.value, str):
            raise ValidationException(f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if len(self.value) > max_length:
            raise ValidationException(f'The {self.prop} must be less than {max_length} characters')
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not True and False:
            raise ValidationException(f'The {self.prop} must be a boolean')
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar('PropsValidated')


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields
    validated_data: PropsValidated

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(Generic[PropsValidated], ValidatorFieldsInterface[PropsValidated]):
    def validate(self, serializer: Serializer):
        is_valid = serializer.is_valid()
        if not is_valid:
            self.errors = {
                field: [str(_error) for _error in _errors]
                for field, _errors in serializer.errors.items()
            }
            return False
        self.validated_data = serializer.validated_data
        return True
