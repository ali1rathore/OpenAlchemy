from sqlalchemy.ext.declarative import declarative_base
from yaml import safe_load

from openapi_sqlalchemy import init_model_factory

Base = declarative_base()
with open("all-of-example-spec.yml") as spec_file:
    SPEC = safe_load(spec_file)
MODEL_FACTORY = init_model_factory(base=Base, spec=SPEC)


Division = MODEL_FACTORY(name="Division")
Employee = MODEL_FACTORY(name="Employee")
