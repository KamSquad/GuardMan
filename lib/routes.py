from lib.functions import test_func, login_func, hash_pass_func
from lib.network import schemas

routes = {'test': test_func,
          'login': login_func,
          'hash_pass': hash_pass_func}


def search_route(input_dictionary):
    for route_key in routes:
        if schemas.check_schema(schema=schemas.schemas[route_key], dict_object=input_dictionary):
            return routes[route_key]
    return None
