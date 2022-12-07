from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.__seedwork.domain.entity import Entity
from src.__seedwork.domain.validators import ValidatorRules


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())

    def __new__(cls, *args, **kwargs):
        cls.validate(name=kwargs.get('name'),
                     description=kwargs.get('description'),
                     is_active=kwargs.get('is_active')
                     )
        return super(Category, cls).__new__(cls)

    def update(self, name, description):
        self.validate(name, description)
        self._set('name', name)
        self._set('description', description)

    def activate(self):
        self._set('is_active', True)

    def deactivate(self):
        self._set('is_active', False)

    @staticmethod
    def validate(name: str, description: str, is_active: bool = None):
        ValidatorRules.values(name, "name").required().string().max_length(255)
        ValidatorRules.values(description, "description").string()
        ValidatorRules.values(is_active, "is_active").boolean()
