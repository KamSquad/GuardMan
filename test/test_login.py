import sys
import json
import socket


def get_socket_answer(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 2288))
    client.send(content)
    resp = client.recv(1024).decode('utf-8')
    if resp:
        return resp
        # queue_res.put(resp)
    else:  # TODO: fill else if empty/None answer
        return 'empty'


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]

    auth_request_login = {'request': 'login',
                          'body': username}

    check_pass_request = {'request': 'hash_pass',
                          'body': {'username': username,
                                   'pass': ''
                                   }
                          }

    req_dict = {'request': 'login',
                'body': username}
    content = json.dumps(req_dict).encode('utf-8')

    answer = get_socket_answer(request=content)
    print(answer)
    salt = json.loads(answer)['body']

    # print()
