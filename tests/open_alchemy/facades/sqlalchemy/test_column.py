"""Tests for SQLAlchemy column facade."""

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import types
from open_alchemy.facades.sqlalchemy import column


@pytest.mark.parametrize(
    "name, expected_value",
    [
        ("Column", sqlalchemy.Column),
        ("Type", sqlalchemy.sql.type_api.TypeEngine),
        ("ForeignKey", sqlalchemy.ForeignKey),
        ("Integer", sqlalchemy.Integer),
        ("BigInteger", sqlalchemy.BigInteger),
        ("Number", sqlalchemy.Float),
        ("String", sqlalchemy.String),
        ("Binary", sqlalchemy.LargeBinary),
        ("Date", sqlalchemy.Date),
        ("DateTime", sqlalchemy.DateTime),
        ("Boolean", sqlalchemy.Boolean),
    ],
    ids=[
        "Column",
        "Type",
        "ForeignKey",
        "Integer",
        "BigInteger",
        "Number",
        "String",
        "Binary",
        "Date",
        "DateTime",
        "Boolean",
    ],
)
@pytest.mark.facade
def test_mapping(name, expected_value):
    """
    GIVEN name and expected value
    WHEN the name is retrieved from column
    THEN the expected value is returned.
    """
    returned_value = getattr(column, name)

    assert returned_value == expected_value


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", sqlalchemy.Integer),
        ("number", sqlalchemy.Float),
        ("string", sqlalchemy.String),
        ("boolean", sqlalchemy.Boolean),
    ],
    ids=["integer", "number", "string", "boolean"],
)
@pytest.mark.facade
def test_construct(type_, expected_type):
    """
    GIVEN artifacts for a type
    WHEN construct is called with the artifacts
    THEN a column with the expected type is returned.
    """
    artifacts = types.ColumnArtifacts(type_)

    returned_column = column.construct(artifacts=artifacts)

    assert isinstance(returned_column, sqlalchemy.Column)
    assert isinstance(returned_column.type, expected_type)
    assert len(returned_column.foreign_keys) == 0
    assert returned_column.nullable is True


@pytest.mark.facade
def test_construct_foreign_key():
    """
    GIVEN artifacts with foreign key
    WHEN construct is called with the artifacts
    THEN a column with a foreign key is returned.
    """
    artifacts = types.ColumnArtifacts("integer", foreign_key="table.column")

    returned_column = column.construct(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('table.column')"


@pytest.mark.parametrize("nullable", [True, False], ids=["true", "false"])
@pytest.mark.facade
def test_construct_nullable(nullable):
    """
    GIVEN value for nullable
    WHEN construct is called with the artifacts with nullable
    THEN the returned column nullable property is equal to nullable.
    """
    artifacts = types.ColumnArtifacts("integer", nullable=nullable)

    returned_column = column.construct(artifacts=artifacts)

    assert returned_column.nullable == nullable


@pytest.mark.parametrize(
    "primary_key", [None, True, False], ids=["none", "true", "false"]
)
@pytest.mark.facade
def test_construct_primary_key(primary_key):
    """
    GIVEN value for primary_key
    WHEN construct is called with the artifacts with primary_key
    THEN the returned column primary_key property is equal to primary_key.
    """
    artifacts = types.ColumnArtifacts("integer", primary_key=primary_key)

    returned_column = column.construct(artifacts=artifacts)

    assert returned_column.primary_key == primary_key


@pytest.mark.parametrize(
    "autoincrement", [None, True, False], ids=["none", "true", "false"]
)
@pytest.mark.facade
def test_construct_autoincrement(autoincrement):
    """
    GIVEN value for autoincrement
    WHEN construct is called with the artifacts with autoincrement
    THEN the returned column autoincrement property is equal to autoincrement.
    """
    artifacts = types.ColumnArtifacts("integer", autoincrement=autoincrement)

    returned_column = column.construct(artifacts=artifacts)

    assert returned_column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [None, True, False], ids=["none", "true", "false"])
@pytest.mark.facade
def test_construct_index(index):
    """
    GIVEN value for index
    WHEN construct is called with the artifacts with index
    THEN the returned column index property is equal to index.
    """
    artifacts = types.ColumnArtifacts("integer", index=index)

    returned_column = column.construct(artifacts=artifacts)

    assert returned_column.index == index


@pytest.mark.parametrize("unique", [None, True, False], ids=["none", "true", "false"])
@pytest.mark.facade
def test_construct_unique(unique):
    """
    GIVEN value for unique
    WHEN construct is called with the artifacts with unique
    THEN the returned column unique property is equal to unique.
    """
    artifacts = types.ColumnArtifacts("integer", unique=unique)

    returned_column = column.construct(artifacts=artifacts)

    assert returned_column.unique == unique


class TestDetermineType:
    """Tests for _determine_type."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_unsupported():
        """
        GIVEN artifacts with an unsupported type
        WHEN _determine_type is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = types.ColumnArtifacts("unsupported")

        with pytest.raises(exceptions.FeatureNotImplementedError):
            column._determine_type(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "type_, expected_type",
        [
            ("integer", sqlalchemy.Integer),
            ("number", sqlalchemy.Float),
            ("string", sqlalchemy.String),
            ("boolean", sqlalchemy.Boolean),
        ],
        ids=["integer", "number", "string", "boolean"],
    )
    @pytest.mark.facade
    def test_supported(type_, expected_type):
        """
        GIVEN type
        WHEN _determine_type is called with the artifacts with the type
        THEN the expected type is returned.
        """
        artifacts = types.ColumnArtifacts(type_)

        returned_type = column._determine_type(artifacts=artifacts)

        assert returned_type == expected_type


class TestHandleInteger:
    """Tests for _handle_integer."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_invalid_format():
        """
        GIVEN artifacts with format that is not supported
        WHEN _handle_integer is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = types.ColumnArtifacts("integer", format="unsupported")

        with pytest.raises(exceptions.FeatureNotImplementedError):
            column._handle_integer(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_integer",
        [
            (None, sqlalchemy.Integer),
            ("int32", sqlalchemy.Integer),
            ("int64", sqlalchemy.BigInteger),
        ],
        ids=["None", "int32", "int64"],
    )
    @pytest.mark.facade
    def test_valid(format_, expected_integer):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_integer is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = types.ColumnArtifacts("integer", format=format_)

        integer = column._handle_integer(artifacts=artifacts)

        assert integer == expected_integer


class TestHandleNumber:
    """Tests for _handle_number."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_invalid_format():
        """
        GIVEN artifacts with format that is not supported
        WHEN _handle_number is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = types.ColumnArtifacts("number", format="unsupported")

        with pytest.raises(exceptions.FeatureNotImplementedError):
            column._handle_number(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_number",
        [(None, sqlalchemy.Float), ("float", sqlalchemy.Float)],
        ids=["None", "float"],
    )
    @pytest.mark.facade
    def test_valid(format_, expected_number):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_integer is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = types.ColumnArtifacts("number", format=format_)

        number = column._handle_number(artifacts=artifacts)

        assert number == expected_number


class TestHandleString:
    """Tests for _handle_string."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_invalid_format():
        """
        GIVEN artifacts with format that is not supported
        WHEN _handle_string is called with the artifacts
        THEN FeatureNotImplementedError is raised.
        """
        artifacts = types.ColumnArtifacts("string", format="unsupported")

        with pytest.raises(exceptions.FeatureNotImplementedError):
            column._handle_string(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_type",
        [
            (None, sqlalchemy.String),
            ("date", sqlalchemy.Date),
            ("date-time", sqlalchemy.DateTime),
            ("byte", sqlalchemy.String),
            ("password", sqlalchemy.String),
            ("binary", sqlalchemy.LargeBinary),
        ],
        ids=["None", "date", "date-time", "byte", "password", "binary"],
    )
    @pytest.mark.facade
    def test_valid(format_, expected_type):
        """
        GIVEN artifacts and expected SQLALchemy type
        WHEN _handle_integer is called with the artifacts
        THEN the expected type is returned.
        """
        artifacts = types.ColumnArtifacts("string", format=format_)

        string = column._handle_string(artifacts=artifacts)

        assert string == expected_type

    @staticmethod
    @pytest.mark.parametrize(
        "format_, expected_type",
        [(None, sqlalchemy.String), ("binary", sqlalchemy.LargeBinary)],
        ids=["string", "binary"],
    )
    @pytest.mark.facade
    def test_valid_max_length(format_, expected_type):
        """
        GIVEN artifacts with max_length and given format
        WHEN _handle_string is called with the artifacts
        THEN a given expected type column with a maximum length is returned.
        """
        length = 1
        artifacts = types.ColumnArtifacts("string", max_length=length, format=format_)

        string = column._handle_string(artifacts=artifacts)

        assert isinstance(string, expected_type)
        assert string.length == length


class TestHandleBoolean:
    """Tests for _handle_boolean."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.facade
    def test_valid():
        """
        GIVEN artifacts
        WHEN _handle_boolean is called with the artifacts
        THEN the boolean type is returned.
        """
        artifacts = types.ColumnArtifacts("boolean")

        boolean = column._handle_boolean(artifacts=artifacts)

        assert boolean == sqlalchemy.Boolean