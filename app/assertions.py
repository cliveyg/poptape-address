import os.path
import json
from jsonschema import validate, draft7_format_checker

def assert_valid_schema(data, schema_file):
    # checks whether the given data matches the schema

    schema = _load_json_schema(schema_file)
    return validate(data, schema, format_checker=draft7_format_checker)


def _load_json_schema(filename):
    # loads the given schema file
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath) as schema_file:
        return json.loads(schema_file.read())
