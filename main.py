from pprint import PrettyPrinter

from server import serializer
from server import graph_checker

from server import server

if __name__ == "__main__":
    # server.run_server()

    pp = PrettyPrinter()
    with open('./server/input_sample.txt') as file:
        message = file.read()

    server.handle_data(message)
    #
    # extracted = serializer.extract_string(message)
    # print(extracted)
    #
    # series = serializer.text_to_series(extracted)
    # print(series)
    #
    # checked = graph_checker.check_series(series)
    # pp.pprint(checked)
