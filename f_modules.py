from schema import Schema, And, Use

from lib.network import net_request


def test_func(*args):
    result = net_request.make_answer_json(answer_code=net_request.answer_codes['success'],
                                          body='ping: ok')
    return result


def login_func(*args):
    request_json, ldb = args
    res_user_id = ldb.check_user_exist(user_name=request_json['body']['username'])
    if res_user_id:
        salt = ldb.gen_and_save_user_salt(user_id=res_user_id)
        result = net_request.make_answer_json(answer_code=net_request.answer_codes['object_created'],
                                              body=salt)
    else:
        result = net_request.make_answer_json(answer_code=net_request.answer_codes['login_failed'],
                                              body='login failed')
    return result


def hash_pass_func(*args):
    request_json, ldb = args
    result = None
    check_pass_res = ldb.check_user_hash_pass(user_name=request_json['body']['username'],
                                              inp_hash_pass=request_json['body']['pass'])
    if check_pass_res:
        token = ldb.gen_and_save_token(user_name=request_json['body']['username'])
        if token:
            # success
            result = net_request.make_answer_json(answer_code=net_request.answer_codes['object_created'],
                                                  body=token)
        else:
            # fail
            result = net_request.make_answer_json(answer_code=net_request.answer_codes['failed'],
                                                  body='create token error')
    if result is None:
        # fail
        result = net_request.make_answer_json(answer_code=net_request.answer_codes['failed'],
                                              body='password incorrect')
    return result


routes = {'test': test_func,
          'login': login_func,
          'hash_pass': hash_pass_func}


schemas = {'test': Schema({'request': 'test'}),
           'login': Schema({'request': 'login',
                            'body': {
                                'username': And(Use(str))}
                            }),
           'hash_pass': Schema({'request': 'hash_pass',
                                'body': {
                                    'username': And(Use(str)),
                                    'pass': And(Use(str))}
                                })
           }
