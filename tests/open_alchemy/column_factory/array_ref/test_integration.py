"""Integration tests for array references."""

import pytest

from open_alchemy.column_factory import array_ref


@pytest.mark.column
def test_handle_array():
    """
    GIVEN schema with array referencing another schema and schemas
    WHEN handle_array is called
    THEN relationship is returned pointing to the referenced schema.
    """
    tablename = "schema"
    schema = {
        "type": "array",
        "items": {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-backref": "schema"},
            ]
        },
    }
    schemas = {
        "RefSchema": {"type": "object", "x-tablename": "ref_schema", "properties": {}}
    }
    logical_name = "ref_schema"
    model_name = "Schema"
    model_schema = {
        "type": "object",
        "x-tablename": tablename,
        "properties": {"id": {"type": "integer"}},
    }

    ([(tbl_logical_name, relationship)], return_schema) = array_ref.handle_array(
        schema=schema,
        model_schema=model_schema,
        schemas=schemas,
        logical_name=logical_name,
    )

    assert relationship.argument == "RefSchema"
    assert relationship.backref == ("schema", {"uselist": None})
    assert relationship.secondary is None
    assert tbl_logical_name == logical_name
    assert return_schema == {
        "type": "array",
        "items": {"type": "object", "x-de-$ref": "RefSchema"},
    }
    assert schemas == {
        "RefSchema": {
            "allOf": [
                {"type": "object", "x-tablename": "ref_schema", "properties": {}},
                {
                    "type": "object",
                    "properties": {
                        f"{tablename}_id": {
                            "type": "integer",
                            "x-foreign-key": f"{tablename}.id",
                            "x-dict-ignore": True,
                        }
                    },
                },
                {
                    "type": "object",
                    "x-backrefs": {
                        "schema": {"type": "object", "x-de-$ref": model_name}
                    },
                },
            ]
        }
    }

    assert False
