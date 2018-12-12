# todo: Correct prepared and prepare the rest of the documentation!

from server import server

if __name__ == "__main__":
    # todo: move file test into tests.py and always just run the server
    while True:
        user_in = input("--- CHOOSE AN OPTION ---\n"
                        "\t0. Exit\n"
                        "\t1. Run server\n"
                        "\t2. Read from input_sample.txt\n")
        if user_in == '0':
            break
        elif user_in == '1':
            server.run_server()
        elif user_in == '2':
            with open('./server/input_sample.txt') as file:
                message = file.read()

            resp = server.handle_data(message)
            continue
        else:
            print("Invalid number was chosen! Try again.")

    print("Thank you for using our script. ;)")
