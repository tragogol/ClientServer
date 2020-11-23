import socket

print("Print \"Roll\" for roll\nPrint \"Exit\" for Exit\n")
try:
    input_command = None
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        print('connecting to %s port %s' % server_address)
        sock.connect(server_address)

        data = sock.recv(128).decode()
        print('received "%s"' % data, end='\n')

        if data == "You are out of credits":
            sock.close()
            break

        print("Send message")
        input_command = input()

        if str(input_command).lower() == "roll":
            print("Print number from 0 to 6")
            sock.sendall(str(input_command).lower().encode())
            data = sock.recv(128).decode()
            input_command_num = input()
            print(data)
            if 0 <= int(input_command_num) <= 6:
                print("Choose color where 0 - black, 1 - red")
                input_command_col = input()
                sock.sendall(str(input_command_num).encode())
                data = sock.recv(128).decode()
                print(data)

                if 0 <= int(input_command_col) <= 1:
                    sock.sendall(str(input_command_col).encode())
                    data = sock.recv(128).decode()
                    print(data)
                else:
                    if int(input_command_col) < 0 or int(input_command_col) > 1:
                        print("Out of range")
                        sock.close()
                        break
            else:
                if int(input_command_num) < 0 or int(input_command_num) > 6:
                    print("Out of range")
                    sock.close()
                    break
        else:
            print("Unknown command")

        if str(input_command).lower() != "exit":
            sock.close()
except ValueError:
    print("Wrong format")

finally:
    print('closing socket')
