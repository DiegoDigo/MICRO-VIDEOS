import json
import uuid
from abc import ABC
from dataclasses import field, dataclass, fields

from src.__seedwork.domain.exceptions import InvalidUuidException


@dataclass(frozen=True)
class ValueObject(ABC):

    def __str__(self) -> str:
        fields_name = [f.name for f in fields(self)]
        return str(getattr(self, fields_name[0])) \
            if len(fields_name) == 1 \
            else json.dumps({field_name: getattr(self, field_name) for field_name in fields_name})


@dataclass(frozen=True)
class UniqueEntityId(ValueObject):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        _id = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', _id)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException() from ex


