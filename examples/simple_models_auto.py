"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,useless-super-delegation

import typing

from open_alchemy import models


class Employee(models.Employee):
    """Employee SQLAlchemy model."""

    id: int
    name: str
    division: str
    salary: typing.Optional[float]

    def from_dict(self, **kwargs: typing.Any) -> "Employee":
        """Construct from a dictionary (eg. a POST payload)."""
        super().from_dict(**kwargs)

    def to_dict(self) -> "EmployeeDict":
        """Convert to a dictionary (eg. to send back for a GET request)."""
        super().to_dict()
