"""Tests for the association pre-processor."""

import pytest

from open_alchemy.schemas import association


class TestRequiresAssociation:
    """Tests for _requires_association."""

    # pylint: disable=protected-access

    TESTS = [
        pytest.param(
            {"type": "integer"},
            {},
            False,
            id="simple",
        ),
        pytest.param(
            {"type": "object"},
            {},
            False,
            id="relationship not many-to-many",
        ),
        pytest.param(
            {"type": "array", "items": {"x-secondary": "association"}},
            {},
            True,
            id="relationship many-to-many",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize("schema, schemas, expected_result", TESTS)
    @pytest.mark.schemas
    @pytest.mark.association
    def test_(schema, schemas, expected_result):
        """
        GIVEN schema, schemas and expected result
        WHEN _requires_association is called with the schema and schemas
        THEN the expected result is returned.
        """
        returned_result = association._requires_association(schemas, schema)

        assert returned_result == expected_result
