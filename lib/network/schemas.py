from schema import SchemaError


def check_schema(schema, dict_object):
    try:
        schema.validate(dict_object)
        return True
    except SchemaError:
        return False
