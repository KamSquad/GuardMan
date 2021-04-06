#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import logging
import os
import json

from lib.routes import r_map
from lib.network import net_request
from lib.db import echo
from lib import config
from lib.network import mserver
import f_modules

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

        # get json object
        request_json = json.loads(request_obj.decode('utf-8'))
        # print(request_obj)

        # check and find route by schema
        route_function = r_map.search_route(input_dictionary=request_json,
                                            routes=f_modules.routes,
                                            request_schemas=f_modules.schemas)
        if route_function:
            result = route_function(request_json, ldb)
        else:
            result = net_request.make_answer_json(answer_code=net_request.answer_codes['failed'],
                                                  body='request format error')
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
