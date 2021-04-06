from schema import SchemaError, Schema, And, Use

schemas = {'test': Schema({'request': 'test'}),
           'login': Schema({'request': And(Use(str)),
                            'body': And(Use(str))
                            }),
           'hash_pass': Schema({'request': 'hash_pass',
                                'body': {
                                    'username': And(Use(str)),
                                    'pass': And(Use(str))}
                                })
           }


def check_schema(schema, dict_object):
    try:
        schema.validate(dict_object)
        return True
    except SchemaError:
        return False
