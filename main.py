#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import logging
import os
import json

from lib.network import request
from lib.db import echo
from lib import config
from lib.network import mserver

config = config.JsonConfig('./config.json')
log = logging.getLogger(__name__)
SERVER_ADDRESS = (HOST, PORT) = '', config.value['mservice']['port']
REQUEST_QUEUE_SIZE = 1


def handle_request(client):
    """
    Main microservice function to parse input requests
    :param client:
    :return:
    """
    log.debug('Child PID: {pid}. Parent PID {ppid}'.format(
        pid=os.getpid(),
        ppid=os.getppid()
    ))
    while True:
        request_obj = client.recv(1024)
        if not request_obj:
            break

        # print('ok')
        request_json = json.loads(request_obj.decode('utf-8'))
        # print(request_obj)

        if 'request' in request_json:  # check request object exist
            # TEST
            if request_json['request'] == 'test':
                result = request.make_answer_json(answer_code=request.answer_codes['success'],
                                                  body='ping: ok')
            # USER LOGIN REQUEST
            # request_json = {'request': 'login',
            #                 'value': 'username'
            #                 }
            elif request_json['request'] == 'login' and 'body' in request_json:
                res_user_id = ldb.check_user_exist(user_name=request_json['body'])
                if res_user_id:
                    salt = ldb.gen_and_save_user_salt(user_id=res_user_id)
                    result = request.make_answer_json(answer_code=request.answer_codes['object_created'],
                                                      body=salt)
            # USER HASH_PASS REQUEST
            # request_json = {'request': 'hash_pass',
            #                 'value': {'username': 'username',
            #                           'pass': 'hashed_with_salt_pass'
            #                           }
            #                 }
            elif request_json['request'] == 'hash_pass' and 'body' in request_json:
                result = None
                check_pass_res = ldb.check_user_hash_pass(user_name=request_json['body']['username'],
                                                          inp_hash_pass=request_json['body']['pass'])
                if check_pass_res:
                    token = ldb.gen_and_save_token(user_name=request_json['body']['username'])
                    if token:
                        # success
                        result = request.make_answer_json(answer_code=request.answer_codes['object_created'],
                                                          body=token)
                    else:
                        # fail
                        result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                                          body='create token error')
                if result is None:
                    # fail
                    result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                                      body='password incorrect')
            else:
                result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                                  body='request format error')
        else:
            # fail
            result = request.make_answer_json(answer_code=request.answer_codes['failed'],
                                              body='no request header')

        # send answer to request
        result = json.dumps(result)
        resp = str(result).encode('utf-8')
        client.send(resp)

    log.info("Closed connection")
    client.close()


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    # db = database.Database()
    ldb = echo.EchoDB(db_host=config.value['db']['host'],
                      db_name=config.value['db']['db_name'],
                      db_user=config.value['db']['db_user'],
                      db_pass=config.value['db']['db_pass'])
    mserver.micro_server(SERVER_ADDRESS, handle_request)

