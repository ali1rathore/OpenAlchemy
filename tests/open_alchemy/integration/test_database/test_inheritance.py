"""Integration tests against database for inheritance."""

import pytest
from sqlalchemy.ext import declarative

import open_alchemy


@pytest.mark.integration
def test_single(engine, sessionmaker):
    """
    GIVEN specification with a schema with single inheritance
    WHEN schema is created and values inserted without id column
    THEN the data is returned as it was inserted with autogenerated value.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Employee": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "x-tablename": "employee",
                    "type": "object",
                    "x-kwargs": {
                        "__mapper_args__": {
                            "polymorphic_on": "type",
                            "polymorphic_identity": "employee",
                        }
                    },
                },
                "Manager": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {"manager_data": {"type": "string"}},
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "manager"}
                            },
                        },
                    ]
                },
                "Engineer": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {"engineer_info": {"type": "string"}},
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "engineer"}
                            },
                        },
                    ]
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    employee = model_factory(name="Employee")
    manager = model_factory(name="Manager")
    engineer = model_factory(name="Engineer")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of models
    employee_instance = employee(id=1, name="employee 1")
    manager_instance = manager(id=2, name="employee 2", manager_data="manager data 2")
    engineer_instance = engineer(
        id=3, name="employee 3", engineer_info="engineer info 3"
    )
    session = sessionmaker()
    session.add(employee_instance)
    session.add(manager_instance)
    session.add(engineer_instance)
    session.flush()

    # Querying session for employee
    queried_employee = session.query(employee).first()
    assert queried_employee.id == 1
    assert queried_employee.name == "employee 1"
    assert queried_employee.type == "employee"
    # Querying session for manager
    queried_manager = session.query(manager).first()
    assert queried_manager.id == 2
    assert queried_manager.name == "employee 2"
    assert queried_manager.type == "manager"
    assert queried_manager.manager_data == "manager data 2"
    # Querying session for engineer
    queried_engineer = session.query(engineer).first()
    assert queried_engineer.id == 3
    assert queried_engineer.name == "employee 3"
    assert queried_engineer.type == "engineer"
    assert queried_engineer.engineer_info == "engineer info 3"


@pytest.mark.integration
def test_joined(engine, sessionmaker):
    """
    GIVEN specification with a schema with joined inheritance
    WHEN schema is created and values inserted without id column
    THEN the data is returned as it was inserted with autogenerated value.
    """
    # Defining specification
    spec = {
        "components": {
            "schemas": {
                "Employee": {
                    "properties": {
                        "id": {"type": "integer", "x-primary-key": True},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "x-tablename": "employee",
                    "type": "object",
                    "x-kwargs": {
                        "__mapper_args__": {
                            "polymorphic_on": "type",
                            "polymorphic_identity": "employee",
                        }
                    },
                },
                "Manager": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-tablename": "manager",
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "x-primary-key": True,
                                    "x-foreign-key": "employee.id",
                                },
                                "manager_data": {"type": "string"},
                            },
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "manager"}
                            },
                        },
                    ]
                },
                "Engineer": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Employee"},
                        {
                            "x-tablename": "engineer",
                            "x-inherits": "Employee",
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "x-primary-key": True,
                                    "x-foreign-key": "employee.id",
                                },
                                "engineer_info": {"type": "string"},
                            },
                            "x-kwargs": {
                                "__mapper_args__": {"polymorphic_identity": "engineer"}
                            },
                        },
                    ]
                },
            }
        }
    }
    # Creating model factory
    base = declarative.declarative_base()
    model_factory = open_alchemy.init_model_factory(spec=spec, base=base)
    employee = model_factory(name="Employee")
    manager = model_factory(name="Manager")
    engineer = model_factory(name="Engineer")

    # Creating models
    base.metadata.create_all(engine)
    # Creating instance of models
    employee_instance = employee(id=1, name="employee 1")
    manager_instance = manager(id=2, name="employee 2", manager_data="manager data 2")
    engineer_instance = engineer(
        id=3, name="employee 3", engineer_info="engineer info 3"
    )
    session = sessionmaker()
    session.add(employee_instance)
    session.add(manager_instance)
    session.add(engineer_instance)
    session.flush()

    # Querying session for employee
    queried_employee = session.query(employee).first()
    assert queried_employee.id == 1
    assert queried_employee.name == "employee 1"
    assert queried_employee.type == "employee"
    # Querying session for manager
    queried_manager = session.query(manager).first()
    assert queried_manager.id == 2
    assert queried_manager.name == "employee 2"
    assert queried_manager.type == "manager"
    assert queried_manager.manager_data == "manager data 2"
    # Querying session for engineer
    queried_engineer = session.query(engineer).first()
    assert queried_engineer.id == 3
    assert queried_engineer.name == "employee 3"
    assert queried_engineer.type == "engineer"
    assert queried_engineer.engineer_info == "engineer info 3"
