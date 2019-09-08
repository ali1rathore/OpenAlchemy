"""Shared fixtures for tests."""

import json
from unittest import mock

import pytest
import sqlalchemy
from sqlalchemy import orm

from openapi_sqlalchemy import column_factory
from openapi_sqlalchemy import helpers
from openapi_sqlalchemy import model_factory


@pytest.fixture
def mocked_sqlalchemy_column(monkeypatch):
    """Monkeypatches sqlalchemy.Column."""
    mock_column = mock.MagicMock()
    monkeypatch.setattr(sqlalchemy, "Column", mock_column)
    return mock_column


@pytest.fixture
def mocked_sqlalchemy_string(monkeypatch):
    """Monkeypatches sqlalchemy.String."""
    mock_string = mock.MagicMock()
    monkeypatch.setattr(sqlalchemy, "String", mock_string)
    return mock_string


@pytest.fixture
def mocked_column_factory(monkeypatch):
    """Monkeypatches column_factory.column_factory."""
    mock_column_factory = mock.MagicMock()
    mock_column_factory.return_value = [("logical name", "SQLAlchemy column")]
    monkeypatch.setattr(column_factory, "column_factory", mock_column_factory)
    return mock_column_factory


@pytest.fixture
def mocked_model_factory(monkeypatch):
    """Monkeypatches model_factory.model_factory."""
    mock_model_factory = mock.MagicMock()
    monkeypatch.setattr(model_factory, "model_factory", mock_model_factory)
    return mock_model_factory


@pytest.fixture
def mocked_resolve_ref(monkeypatch):
    """Monkeypatches helpers.resolve_ref."""
    mock_resolve_ref = mock.MagicMock()
    monkeypatch.setattr(helpers, "resolve_ref", mock_resolve_ref)
    return mock_resolve_ref


@pytest.fixture(scope="function", params=["sqlite:///:memory:"])
def engine(request):
    """Creates a sqlite engine."""
    return sqlalchemy.create_engine(request.param)


@pytest.fixture(scope="function")
def sessionmaker(engine):  # pylint: disable=redefined-outer-name
    """Creates a sqlite session."""
    return orm.sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def args():
    """Arguments."""
    return ("arg1", "arg2")


@pytest.fixture(scope="function")
def kwargs():
    """Keyword arguments."""
    return {"kwarg1": "value 1", "kwarg2": "value 2"}


@pytest.fixture(scope="session")
def testing_env_name():
    """Environment variable name that indicates that tests are running."""
    return "TESTING"


@pytest.fixture(scope="session")
def decorator_trace_env_name():
    """Environment variable name where decorator traces are stored."""
    return "DECORATOR_TRACE"


@pytest.fixture(scope="function", autouse=True)
def set_testing(
    monkeypatch,
    request,
    testing_env_name: str,  # pylint: disable=redefined-outer-name
    decorator_trace_env_name: str,  # pylint: disable=redefined-outer-name
):
    """By default sets TESTING environment variable."""
    # Do not apply TESTING environment variable if test is marked with
    # prod_env
    if "prod_env" in request.keywords:
        return
    monkeypatch.setenv(testing_env_name, "")
    # Setting up tracing of which functions were called
    monkeypatch.setenv(decorator_trace_env_name, json.dumps([]))
