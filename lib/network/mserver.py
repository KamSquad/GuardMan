import os
import signal
import socket

from main import REQUEST_QUEUE_SIZE, log


def micro_server(server_address, handle_request):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = REQUEST_QUEUE_SIZE

    # Create a new socket
    listen_socket = socket.socket(
        address_family,
        socket_type
    )
    # Allow to reuse the same address
    listen_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    # Bind
    listen_socket.bind(server_address)
    # Activate
    listen_socket.listen(request_queue_size)
    log.debug("Parent PID (PPID): {pid}\n".format(pid=os.getpid()))

    signal.signal(signal.SIGCHLD, handle_signal)

    while True:
        # New client connection
        client_connection, client_address = listen_socket.accept()
        # Handle request
        log.info("Start connected %s" % client_address[0])
        pid = os.fork()
        if pid == 0:
            listen_socket.close()  # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            client_connection.close()


def handle_signal(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,
                os.WNOHANG
            )
        except OSError:
            return
        if pid == 0:
            return
        else:
            log.debug('Child PID: {pid} terminated with status {status}'.format(
                pid=pid,
                status=status
            ))
