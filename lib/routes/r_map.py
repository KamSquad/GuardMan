import f_modules
from lib.network import schemas

'''
EXAMPLE:
routes = {'test': test_func,
          'login': login_func,
          'hash_pass': hash_pass_func}
'''


def search_route(input_dictionary, routes, request_schemas):
    for route_key in routes:
        if schemas.check_schema(schema=request_schemas[route_key], dict_object=input_dictionary):
            return routes[route_key]
    return None
