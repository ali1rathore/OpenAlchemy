"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import models


class DivisionDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]


class TDivision(typing.Protocol):
    """
    SQLAlchemy model protocol.

    A part of a company.

    Attrs:
        id: Unique identifier for the division.
        name: The name of the division.
        employees: The employees of the Division.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[int]]'
    name: 'sqlalchemy.Column[typing.Optional[str]]'
    employees: 'sqlalchemy.Column[typing.Sequence["TEmployee"]]'

    def __init__(self, id: typing.Optional[int] = None, name: typing.Optional[str] = None, employees: typing.Optional[typing.Sequence["TEmployee"]] = None) -> None:
        """
        Construct.

        Args:
            id: Unique identifier for the division.
            name: The name of the division.
            employees: The employees of the Division.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None, name: typing.Optional[str] = None) -> "TDivision":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: Unique identifier for the division.
            name: The name of the division.
            employees: The employees of the Division.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TDivision":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> DivisionDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Division: typing.Type[TDivision] = models.Division  # type: ignore


class EmployeeDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]
    division: typing.Optional["DivisionDict"]


class TEmployee(typing.Protocol):
    """
    SQLAlchemy model protocol.

    Person that works for a company.

    Attrs:
        id: Unique identifier for the employee.
        name: The name of the employee.
        division: The division of the Employee.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: 'sqlalchemy.Column[typing.Optional[int]]'
    name: 'sqlalchemy.Column[typing.Optional[str]]'
    division: 'sqlalchemy.Column[typing.Optional["TDivision"]]'

    def __init__(self, id: typing.Optional[int] = None, name: typing.Optional[str] = None, division: typing.Optional["TDivision"] = None) -> None:
        """
        Construct.

        Args:
            id: Unique identifier for the employee.
            name: The name of the employee.
            division: The division of the Employee.

        """
        ...

    @classmethod
    def from_dict(cls, id: typing.Optional[int] = None, name: typing.Optional[str] = None, division: typing.Optional["DivisionDict"] = None) -> "TEmployee":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: Unique identifier for the employee.
            name: The name of the employee.
            division: The division of the Employee.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TEmployee":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> EmployeeDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Employee: typing.Type[TEmployee] = models.Employee  # type: ignore
