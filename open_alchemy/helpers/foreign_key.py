"""Helpers for foreign keys."""

from .. import types
from . import peek
from . import relationship


def calculate_column_name(
    *, type_: relationship.Type, property_schema: types.Schema, schemas: types.Schemas
) -> str:
    """
    Calculate the column name based on the relationship property schema.

    Assume the property is a x-to-one or one-to-many relationship.
    Assume the relationship property schema is valid.

    Args:
        type_: The type of relationship the schema defines.
        property_schema: The schema of the relationship property.
        schemas: All defined schemas used to resolve any $ref.

    Returns:
        The name of the foreign key column.

    """
    assert type_ != relationship.Type.MANY_TO_MANY

    if type_ == relationship.Type.ONE_TO_MANY:
        items_schema = peek.items(schema=property_schema, schemas=schemas)
        assert items_schema is not None
        property_schema = items_schema

    x_foreign_key_column = peek.foreign_key_column(
        schema=property_schema, schemas=schemas
    )
    return x_foreign_key_column if x_foreign_key_column is not None else "id"


def calculate_prop_name(
    *,
    type_: relationship.Type,
    column_name: str,
    property_name: str,
    target_schema: types.Schema,
    schemas: types.Schemas,
) -> str:
    """
    Calculate the foreign key property name based on the relationship type.

    Assume type_ is not a many to many relationship.
    Assume target_schema is a valid model.

    For x-to-one use the column and property name, for one-to-many also use the
    tablename.

    Args:
        type_: The type of relationship.
        column_name: The foreign key column name.
        property_name: The name of the property that defines the relationship.
        target_schema: The schema of the model targeted by the foreign key
            of the relationship.
        schema: All defines schemas used to resolve any $ref.

    Returns:
        The name of the foreign key property.

    """
    assert type_ != relationship.Type.MANY_TO_MANY

    if type_ == relationship.Type.ONE_TO_MANY:
        tablename = peek.tablename(schema=target_schema, schemas=schemas)
        assert tablename is not None
        property_name = f"{tablename}_{property_name}"

    return f"{property_name}_{column_name}"


def calculate_foreign_key(
    *, foreign_key_column_name: str, target_schema: types.Schema, schemas: types.Schemas
) -> str:
    """
    Calculate the foreign key.

    Assume target_schema is a valid model.

    Args:
        foreign_key_column_name: The name of the foreign key column.
        target_schema: The schema of the model targeted by the foreign key
            of the relationship.
        schema: All defines schemas used to resolve any $ref.

    Returns:
        The foreign key.

    """
    tablename = peek.tablename(schema=target_schema, schemas=schemas)
    assert tablename is not None
    return f"{tablename}.{foreign_key_column_name}"
