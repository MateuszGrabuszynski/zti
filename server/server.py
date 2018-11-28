import socket
import sys
import _thread

from . import serializer, graph_checker


def handle_data(data):
    print(f'data: {data}')

    extracted = serializer.extract_string(data)
    print(f'extracted: {extracted}')

    if len(extracted) > 1:
        series = serializer.text_to_series(extracted)
    else:
        series = extracted
    print(f'series: {series}')

    return str(graph_checker.check_words(extracted, series))


def handle_client(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        try:
            response = handle_data(data)
            print(f'response: {response}')
            conn.send(response.encode())
        except Exception as ex:
            print(str(ex))

    conn.close()


def run_server(host='', port=8080, max_conn=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
    except socket.error:
        sys.exit()

    s.listen(max_conn)  # allow max_conn connections at a time

    while True:
        try:
            conn, addr = s.accept()
            print(f"Connected {addr[0]}:{addr[1]}")
            _thread.start_new_thread(handle_client, (conn,))
        except KeyboardInterrupt:
            print("Server closed")
            s.close()
            break
