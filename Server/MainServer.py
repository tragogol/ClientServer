import socket
import random
from datetime import datetime

from Server.IOdata import IOdata


def roll(bet_number, bet_color):
    random.seed(datetime.now())
    number = random.randint(0, 6)
    color = int(random.getrandbits(1))

    if number == int(bet_number) and color == int(bet_color):
        ioClass.change_balance(2)
        return ("Rolled number: " + str(number)
                + "\nRolled Color: " + str(color)
                + "\nYou win")
    else:
        ioClass.change_balance(-2)
        return ("Rolled number: " + str(number)
                + "\nRolled Color: " + str(color)
                + "\nYou lose")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)
client_message = None
while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', str(client_address))
        ioClass = IOdata(client_address[0])
        connection.sendall(ioClass.get_data().encode())

        if ioClass.get_balance() <= 0:
            connection.sendall("You are out of credits".encode())
            connection.close()
            break

        try:
            client_message = connection.recv(128).decode()
        except ConnectionError:
            print(ConnectionError)

        print('received "%s"' % client_message)
        if client_message == "roll":
            connection.sendall("Received".encode())

            roll_number = connection.recv(128).decode()
            if roll_number.isnumeric():
                connection.sendall("Received".encode())
                roll_color = connection.recv(128).decode()
                if roll_color.isnumeric():
                    connection.sendall((roll(int(roll_number), int(roll_color))).encode())
        if client_message == "exit":
            connection.close()

        else:
            connection.sendall("Unknown command".encode())

    except ConnectionError:
        print(ConnectionError)
    finally:
        print("Connection closed")
