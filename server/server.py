""" Contains all server functions."""

import socket
import sys
import _thread

from . import serializer, graph_checker


def handle_data(data):
    """ Allows to handle data sent by the client.

    :param data: Raw data sent by the client.
    :return: Response that may be sent back to the client.
    """
    print(f'--CLIENT SENT:\n{data}')

    address, begin, end = serializer.extract_address(data)
    # todo: this was supposed to be read from nif:beginIndex and nif:endIndex (?)

    extracted = serializer.extract_string(data, begin, end)
    print(f'--EXTRACTED:\n{extracted}')

    if extracted == -1:
        print('Some error occured while extracting')
        return -1

    if len(extracted) > 0:
        series = serializer.text_to_series(extracted, begin, end)
    else:
        series = extracted
    print(f'--SERIES:\n{series}')

    graphed = graph_checker.check_series(series)
    print(f'--GRAPHED:\n{graphed}')

    response = serializer.prepare_response(graphed, data, address)
    print(f'--RESPONSE:\n{response}')
    return response


def handle_client(conn):
    """ Main client handling function. Runs in a new thread while the client is connected to the server.
    Closes the connection when no data is received.

    :param conn: Connection parameters with a connection hook.
    """
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        try:
            response = handle_data(data)
            conn.send(response.encode())
        except Exception as ex:
            print(str(ex))

    conn.close()


def run_server(host='', port=8080, max_conn=10):
    """Allows to run a server

    :param host: Allows to run the server only locally (e.g. 127.0.0.1), empty runs everywhere (like 0.0.0.0).
    :param port: Port on which the server runs.
    :param max_conn: Maximum allowed number of simultaneous incoming connections.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Binding the server on port {port} ({host}).")
        s.bind((host, port))
    except socket.error:
        sys.exit()

    s.listen(max_conn)  # allow max_conn connections at a time

    while True:
        try:
            conn, addr = s.accept()
            print(f"Starting new thread for connection from {addr[0]}:{addr[1]}")
            _thread.start_new_thread(handle_client, (conn,))
        except KeyboardInterrupt:
            s.close()
            print("Server closed")
            break
