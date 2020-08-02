"""Assemble the final schema and return its type."""

import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types

from . import ext_prop as ext_prop_helper
from . import ref as ref_helper


class PeekValue(types.Protocol):
    """Defines interface for peek functions."""

    def __call__(self, *, schema: types.Schema, schemas: types.Schemas) -> typing.Any:
        """Call signature for peek functions."""
        ...


def type_(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the type of the schema.

    Raises TypeMissingError if the final schema does not have a type or the value is
    not a string.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        The type of the schema.

    """
    value = peek_key(schema=schema, schemas=schemas, key="type")
    if value is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(value, str):
        raise exceptions.TypeMissingError(
            "A type property value must be of type string."
        )
    return value


def nullable(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the nullable property from a property schema.

    Raises MalformedSchemaError if the nullable value is not a boolean.

    Args:
        schema: The schema to get the nullable from.
        schemas: The schemas for $ref lookup.

    Returns:
        The nullable value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="nullable")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A nullable value must be of type boolean."
        )
    return value


def format_(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the format property from a property schema.

    Raises MalformedSchemaError if the format value is not a string.

    Args:
        schema: The schema to get the format from.
        schemas: The schemas for $ref lookup.

    Returns:
        The format value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="format")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError("A format value must be of type string.")
    return value


def autoincrement(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Retrieve the autoincrement property from a property schema.

    Raises MalformedSchemaError if the autoincrement value is not a boolean.

    Args:
        schema: The schema to get the autoincrement from.
        schemas: The schemas for $ref lookup.

    Returns:
        The autoincrement value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-autoincrement")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A autoincrement value must be of type boolean."
        )
    return value


def index(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the index property from a property schema.

    Raises MalformedSchemaError if the index value is not a boolean.

    Args:
        schema: The schema to get the index from.
        schemas: The schemas for $ref lookup.

    Returns:
        The index value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-index")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError("A index value must be of type boolean.")
    return value


def unique(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the unique property from a property schema.

    Raises MalformedSchemaError if the unique value is not a boolean.

    Args:
        schema: The schema to get the unique from.
        schemas: The schemas for $ref lookup.

    Returns:
        The unique value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-unique")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError("A unique value must be of type boolean.")
    return value


def max_length(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[int]:
    """
    Retrieve the maxLength property from a property schema.

    Raises MalformedSchemaError if the maxLength value is not an integer.

    Args:
        schema: The schema to get the maxLength from.
        schemas: The schemas for $ref lookup.

    Returns:
        The maxLength value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="maxLength")
    if value is None:
        return None
    if not isinstance(value, int):
        raise exceptions.MalformedSchemaError(
            "A maxLength value must be of type integer."
        )
    return value


def read_only(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Determine whether schema is readOnly.

    Raises MalformedSchemaError if the readOnly value is not a boolean.

    Args:
        schema: The schema to get readOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is readOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="readOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must be of type boolean."
        )
    return value


def write_only(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Determine whether schema is writeOnly.

    Raises MalformedSchemaError if the writeOnly value is not a boolean.

    Args:
        schema: The schema to get writeOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is writeOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="writeOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A writeOnly property must be of type boolean."
        )
    return value


def description(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the description property from a property schema.

    Raises MalformedSchemaError if the description value is not a string.

    Args:
        schema: The schema to get the description from.
        schemas: The schemas for $ref lookup.

    Returns:
        The description value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="description")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "A description value must be of type string."
        )
    return value


def primary_key(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether property schema is for a primary key.

    Raises MalformedSchemaError if the x-primary-key value is not a boolean.

    Args:
        schema: The schema to get x-primary-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is for a primary key property.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-primary-key")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-primary-key property must be of type boolean."
        )
    return value


def tablename(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the tablename of the schema.

    Raises MalformedSchemaError if the tablename value is not a string.

    Args:
        schema: The schema to get tablename from.
        schemas: The schemas for $ref lookup.

    Returns:
        The tablename or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-tablename")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-tablename property must be of type string."
        )
    return value


def inherits(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.Union[str, bool]]:
    """
    Retrieve the value of the x-inherits extension property of the schema.

    Raises MalformedSchemaError if the value is not a string nor a boolean.

    Args:
        schema: The schema to get x-inherits from.
        schemas: The schemas for $ref lookup.

    Returns:
        The inherits or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-inherits")
    if value is None:
        return None
    if not isinstance(value, (str, bool)):
        raise exceptions.MalformedSchemaError(
            "The x-inherits property must be of type string or boolean."
        )
    return value


def json(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the value of the x-json extension property of the schema.

    Raises MalformedSchemaError if the value is not a boolean.

    Args:
        schema: The schema to get x-json from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-json value or None if the schema does not have the key.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-json")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-json property must be of type boolean."
        )
    return value


def backref(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the backref of the schema.

    Raises MalformedSchemaError if the backref value is not a string.

    Args:
        schema: The schema to get backref from.
        schemas: The schemas for $ref lookup.

    Returns:
        The backref or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-backref")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-backref property must be of type string."
        )
    return value


def secondary(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the secondary of the schema.

    Raises MalformedSchemaError if the secondary value is not a string.

    Args:
        schema: The schema to get secondary from.
        schemas: The schemas for $ref lookup.

    Returns:
        The secondary or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-secondary")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-secondary property must be of type string."
        )
    return value


def uselist(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the uselist of the schema.

    Raises MalformedSchemaError if the uselist value is not a boolean.

    Args:
        schema: The schema to get uselist from.
        schemas: The schemas for $ref lookup.

    Returns:
        The uselist or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-uselist")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-uselist property must be of type boolean."
        )
    return value


def items(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[dict]:
    """
    Retrieve the items of the schema.

    Raises MalformedSchemaError if the items value is not a dictionary.

    Args:
        schema: The schema to get items from.
        schemas: The schemas for $ref lookup.

    Returns:
        The items or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="items")
    if value is None:
        return None
    if not isinstance(value, dict):
        raise exceptions.MalformedSchemaError(
            "The items property must be of type dict."
        )
    return value


def _check_kwargs(*, value: typing.Any, key: str) -> typing.Dict[str, typing.Any]:
    """Check the kwargs value."""
    # Check value
    if not isinstance(value, dict):
        raise exceptions.MalformedSchemaError(
            f"The {key} property must be of type dict."
        )
    # Check keys
    not_str_keys = filter(lambda key: not isinstance(key, str), value.keys())
    if next(not_str_keys, None) is not None:
        raise exceptions.MalformedSchemaError(
            f"The {key} property must have string keys."
        )
    return value


def kwargs(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """
    Retrieve the x-kwargs of the schema.

    Raises MalformedSchemaError if the x-kwargs value is not a dictionary.

    Args:
        schema: The schema to get x-kwargs from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-kwargs or None.

    """
    key = "x-kwargs"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    return _check_kwargs(value=value, key=key)


def foreign_key_kwargs(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[dict]:
    """
    Retrieve the x-foreign-key-kwargs of the schema.

    Raises MalformedSchemaError if the x-foreign-key-kwargs value is not a dictionary.

    Args:
        schema: The schema to get x-foreign-key-kwargs from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-foreign-key-kwargs or None.

    """
    key = "x-foreign-key-kwargs"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    return _check_kwargs(value=value, key=key)


def ref(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the $ref of the schema.

    Raises MalformedSchemaError if the $ref value is not a dictionary.

    Args:
        schema: The schema to get $ref from.
        schemas: The schemas for $ref lookup.

    Returns:
        The $ref or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="$ref")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The $ref property must be of type string."
        )
    return value


def foreign_key(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the foreign-key of the schema.

    Raises MalformedSchemaError if the foreign-key value is not a string.

    Args:
        schema: The schema to get foreign-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        The foreign-key or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-foreign-key")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-foreign-key property must be of type string."
        )
    return value


def foreign_key_column(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the foreign-key-column of the schema.

    Raises MalformedSchemaError if the foreign-key-column value is not a string.

    Args:
        schema: The schema to get foreign-key-column from.
        schemas: The schemas for $ref lookup.

    Returns:
        The foreign-key-column or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-foreign-key-column")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-foreign-key-column property must be of type string."
        )
    return value


def composite_index(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.List]:
    """
    Retrieve the x-composite-index of the schema.

    Raises MalformedExtensionPropertyError if the x-composite-index value does not
        conform with the schema.

    Args:
        schema: The schema to get x-composite-index from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-composite-index or None.

    """
    key = "x-composite-index"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    ext_prop_helper.get(source={key: value}, name=key)  # type: ignore
    return value


def composite_unique(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.List]:
    """
    Retrieve the x-composite-unique of the schema.

    Raises MalformedExtensionPropertyError if the x-composite-unique value does not
        conform with the schema.

    Args:
        schema: The schema to get x-composite-unique from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-composite-unique or None.

    """
    key = "x-composite-unique"
    value = peek_key(schema=schema, schemas=schemas, key=key)
    if value is None:
        return None
    # Check value
    ext_prop_helper.get(source={key: value}, name=key)  # type: ignore
    return value


def default(*, schema: types.Schema, schemas: types.Schemas) -> types.TColumnDefault:
    """
    Retrieve the default value and check it against the schema.

    Args:
        schema: The schema to retrieve the default value from.

    """
    # Retrieve value
    value = peek_key(schema=schema, schemas=schemas, key="default")
    if value is None:
        return None
    # Assemble schema
    resolved_schema: types.ColumnSchema = {
        "type": type_(schema=schema, schemas=schemas)
    }
    format_value = format_(schema=schema, schemas=schemas)
    max_length_value = max_length(schema=schema, schemas=schemas)
    if format_value is not None:
        resolved_schema["format"] = format_value
    if max_length_value is not None:
        resolved_schema["maxLength"] = max_length_value
    try:
        facades.jsonschema.validate(value, resolved_schema)
    except facades.jsonschema.ValidationError:
        raise exceptions.MalformedSchemaError(
            "The default value does not conform to the schema. "
            f"The value is: {repr(value)}"
        )
    return value


def peek_key(*, schema: types.Schema, schemas: types.Schemas, key: str) -> typing.Any:
    """
    Recursive type lookup.

    Raise MalformedSchemaError of a $ref value is seen again.

    Args:
        schema: The schema to look up the key in.
        schemas: All the schemas to resolve any $ref.
        key: The key to check for.
        seen_refs: All the $ref that have already been seen.

    Returns:
        The key value (if found) or None.

    """
    return _peek_key(schema, schemas, key, set())


def _peek_key(
    schema: types.Schema, schemas: types.Schemas, key: str, seen_refs: typing.Set[str]
) -> typing.Any:
    """Implement peek_key."""
    # Check schema and schemas are dict
    if not isinstance(schema, dict):
        raise exceptions.MalformedSchemaError("The schema must be a dictionary.")
    if not isinstance(schemas, dict):
        raise exceptions.MalformedSchemaError("The schemas must be a dictionary.")

    # Base case, look for type key
    value = schema.get(key)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref_value = schema.get("$ref")
    if ref_value is not None:
        # Check that ref is string
        if not isinstance(ref_value, str):
            raise exceptions.MalformedSchemaError("The value of $ref must ba a string.")
        # Check for circular $ref
        if ref_value in seen_refs:
            raise exceptions.MalformedSchemaError("Circular reference detected.")
        seen_refs.add(ref_value)

        _, ref_schema = ref_helper.get_ref(ref=ref_value, schemas=schemas)
        return _peek_key(ref_schema, schemas, key, seen_refs)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        # Check value of allOf
        if not isinstance(all_of, list):
            raise exceptions.MalformedSchemaError("The value of allOf must be a list.")

        for sub_schema in all_of:
            # Check value
            if not isinstance(sub_schema, dict):
                raise exceptions.MalformedSchemaError(
                    "The elements of allOf must be dictionaries."
                )

            value = _peek_key(sub_schema, schemas, key, seen_refs)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None


def prefer_local(
    *, get_value: PeekValue, schema: types.Schema, schemas: types.Schemas
) -> typing.Any:
    """
    Retrieve the value using a function preferably without having to follow a $ref.

    1. Check for allOf:
        if found, iterate over schemas in allOf and skip any that contain $ref and
            return the value returned by get_value if it is not None.
    2. Return output of get_value called on the schema.

    Args:
        get_value: The function that knows how to retrieve the value.
        schema: The schema to process.
        schemas: All the schemas.

    Returns:
        The value returned by get_value preferably without following any $ref.

    """
    all_of = schema.get("allOf")
    if all_of is not None:
        no_ref = filter(lambda sub_schema: sub_schema.get("$ref") is None, all_of)

        def map_to_value(sub_schema: types.Schema) -> typing.Any:
            """Use get_value to turn the schema into the value."""
            return get_value(schema=sub_schema, schemas=schemas)

        retrieved_values = map(map_to_value, no_ref)
        not_none_retrieved_values = filter(
            lambda value: value is not None, retrieved_values
        )
        retrieved_value = next(not_none_retrieved_values, None)
        if retrieved_value is not None:
            return retrieved_value
    return get_value(schema=schema, schemas=schemas)
