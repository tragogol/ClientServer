import json
import os
import re


class IOdata:

    def __init__(self, address, json_file_name='client_data.json'):
        self.json_file_name = json_file_name
        self.address = str(address)

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_json_file_name(self):
        return self.json_file_name

    def set_json_file_name(self, json_file_name):
        self.json_file_name = json_file_name

    def get_balance(self):
        with open(self.json_file_name) as f:
            json_object = json.load(f)
            if self.address in json_object:
                return json_object.get(self.address)
            else:
                return None

    def data_checker(self):
        with open(self.json_file_name) as f:
            if os.stat(self.json_file_name).st_size == 0:
                with open(self.json_file_name, 'w') as file:
                    file.write("{}")
                    file.close()

            json_object = json.load(f)
            if self.address not in json_object:
                keyValuePair = {self.address: 100}
                with open(self.json_file_name) as f:
                    data = json.load(f)
                f.close()

                data.update(keyValuePair)
                with open(self.json_file_name, 'w') as f:
                    json.dump(data, f)
                    f.close()
                return "Account created, you have 100 credits"

            elif self.address in json_object:
                return "Your balance: " + str(json_object.get(self.address))

    def change_balance(self, value):
        with open(self.json_file_name, 'r') as file:
            json_data = json.load(file)
            json_data[self.address] = int(self.get_balance() + value)

        with open(self.json_file_name, 'w') as file:
            json.dump(json_data, file)
            print("Balance Changed")

    def get_data(self):
        return self.data_checker()
