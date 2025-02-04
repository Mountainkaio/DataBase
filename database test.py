
from sys import exit as ex
from random import randint, choice

class DataBase:
    id = 0
    link_user_name_to_password = {}
    password_confirmed = False
    file_path = "users.txt"
    file_path_bank = "bank.txt"
    id_to_usr = {}
    id_contact_list = []

    def __init__(self):
        self.load_from_file()
        self.id_to_usr = self.load_from_file(self.file_path_bank, self.id_to_usr)
        self.set_cls_id_to_last_id()
        self.id = self.give_id()
        self.user_name = ""
        self.password = ""
        self.random_pin = ''
        self.info = ''
        self.access_level = 'user'
        self.balance = 100

    def load_contact_list(self):
        if self.link_user_name_to_password != '':
            self.id_contact_list = self.link_user_name_to_password[self.user_name]['contacts']
        else:
            self.id_contact_list = []

    @classmethod
    def set_cls_id_to_last_id(cls):
        try:
            last_user = list(cls.link_user_name_to_password.keys())[-1]
            cls.id = cls.link_user_name_to_password[last_user]['id']
        except (IndexError, AttributeError, TypeError):
            cls.id = 0

    # Python
    def add_contact(self):
        while True:
            try:
                contact_to_add = int(input("Contact ID\n#"))
            except (ValueError, TypeError):
                print("Invalid input. Please enter a valid numeric ID.")
                continue

            if contact_to_add not in self.id_to_usr:
                print("Contact not found! Try again.")
            elif contact_to_add == self.link_user_name_to_password.get(self.user_name, {}).get('id'):
                print("You can't add your own ID!")
            elif contact_to_add in self.id_contact_list:
                print("This contact is already in your list!")
            else:
                break

            try:
                contact_to_add = int(input("Enter a valid Contact ID\n#"))
            except ValueError:
                print("Invalid input. Please enter a valid numeric ID.")
                return

        self.id_contact_list.append(contact_to_add)
        self.write_on_file(self.link_user_name_to_password)
        contact_name = self.id_to_usr.get(contact_to_add, "Unknown")
        print(f"Contact '{contact_name}' added successfully!")

    def update_bank_txt(self):
        old_data = self.id_to_usr
        self.id_to_usr[self.id] = self.user_name
        self.write_on_file(self.id_to_usr, self.file_path_bank)

    @classmethod
    def erase_db(cls):
        with open(cls.file_path, "w") as file:
            file.write("")
        with open(cls.file_path_bank, "w") as file:
            file.write("")

    @staticmethod
    def ask_for_user_name():
        user_name = input("What\'s your username (spaces will be deleted!)?\n#").strip(" ").lower()
        while user_name == "":
            user_name = input("Please, enter a valid username:\n#").strip(" ").lower()
        return user_name

    @staticmethod
    def ask_for_password(change_password=False):
        password = input("What\'s your password?\n#" if change_password == False else "What's your new password?\n#").strip(" ")
        while password == "":
            password = input("Please, enter a valid password:\n#").strip(" ")
        return password

    @classmethod
    def give_id(cls):
        cls.id += 1
        return cls.id

    def confirm_password(self):
        check_password = input("Confirm your password:\n#").strip(" ").lower()
        return True if check_password == self.password else False

    def add_user(self):
        if self.confirm_password():
            self.link_user_name_to_password[self.user_name] = {'password':self.password, 'balance':self.balance, 'random_pin':self.random_pin, 'access_level':self.access_level, 'id':self.id, 'contacts':self.id_contact_list}
            self.update_bank_txt()
            print("Registered successfully!")
        else:
            ex("Wrong password!")

    def check_user_existence(self):
        return True if self.user_name in self.link_user_name_to_password else False

    @classmethod
    def write_on_file(cls, data, path=file_path):
        with open(path, "w") as file:
            file.write(str(data))

    def transfer(self):
        if not self.id_contact_list:
            if input("Your contact list is empty. Do you want to enter an ID manually? (Y/n):\n#").lower() != "y":
                print("Transfer canceled.")
                return
            else:
                try:
                    id_to_transfer_to = int(input("Transfer to ID:\n#"))
                    if id_to_transfer_to not in self.id_to_usr or id_to_transfer_to == self.id:
                        print("Invalid input!")
                        return
                except ValueError:
                    print("Invalid input. Please enter a valid numeric ID.")
                    return
        else:
            list_or_manual = input("Do you want to choose a contact from your contact list? (Y/n):\n#").lower()
            while list_or_manual not in ["y", "n"]:
                list_or_manual = input("Invalid input!\n#").lower()

            if list_or_manual == "y":
                print("Your contacts:")
                for i, contact in enumerate(self.id_contact_list, start=1):
                    print(f"{i}. {self.id_to_usr.get(contact, 'Unknown')}")
                try:
                    contact_index = int(input("Enter the number of the contact you want to transfer to:\n#")) - 1
                    if contact_index < 0 or contact_index >= len(self.id_contact_list):
                        print("Invalid selection!")
                        return
                    id_to_transfer_to = self.id_contact_list[contact_index]
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    return
            else:
                try:
                    id_to_transfer_to = int(input("Transfer to ID:\n#"))
                    if id_to_transfer_to not in self.id_to_usr or id_to_transfer_to == self.id:
                        print("Invalid input!")
                        return
                except ValueError:
                    print("Invalid input. Please enter a valid numeric ID.")
                    return

        try:
            print(f"Transferring to {self.id_to_usr[id_to_transfer_to]}.")
            amount = int(input(f"How much do you want to transfer? (Balance: {self.balance})\n#"))
            if amount <= 0 or amount > self.balance:
                print("Invalid amount!")
                return

            self.balance -= amount
            self.link_user_name_to_password[self.user_name]['balance'] -= amount
            self.link_user_name_to_password[self.id_to_usr[id_to_transfer_to]]['balance'] += amount
            self.write_on_file(self.link_user_name_to_password)
            print(f"Transferred {amount} to {self.id_to_usr[id_to_transfer_to]} successfully!")
        except ValueError:
            print("Invalid input. Please enter a valid numeric amount.")
            return

    @classmethod
    def load_from_file(cls, path=file_path, var=None):
        try:
            with open(path, "r") as file:
                if path == cls.file_path:
                    cls.link_user_name_to_password = eval(file.read().strip())
                else:
                    var = eval(file.read().strip())
                    return var
        except (FileNotFoundError, SyntaxError):
            if path == cls.file_path:
                cls.link_user_name_to_password = {}
            else:
                var = {}
                return var

    @staticmethod
    def make_random_pin():
        num_of_chars = randint(8, 10)
        alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        nums = [i for i in range(0, 10)]
        password = []
        for i in range(num_of_chars):
            if randint(0, 1) == 0:
                password.append(choice(alphabet) if randint(0,1) == 1 else choice(alphabet).upper())
            else:
                password.append(choice(nums))
        return ''.join(map(str, password))

    def change_password(self):
        print("Changing password...")
        ask_for_random_pin = input("What's your random PIN?\n#").strip(" ")
        while ask_for_random_pin == "":
            ask_for_random_pin = input("Please, enter a valid PIN:\n#").strip(" ")

        if ask_for_random_pin == self.random_pin:
            self.password = self.ask_for_password(True)
            self.link_user_name_to_password[self.user_name]['password'] = self.password
            self.write_on_file(self.link_user_name_to_password)
            print("Password changed successfully!")
        else:
            ex("Wrong PIN!")

    def sign_up(self, proceed_to_login=False):
        print("Signing up...")
        self.user_name = self.ask_for_user_name()
        if self.check_user_existence():
            ex("User already registered!")
        self.password = self.ask_for_password()
        self.random_pin = self.make_random_pin()
        self.add_user()
        print(f"Your random PIN is: {self.random_pin}.\nYou will use this PIN if you need to change your password.\nDO NOT FORGET IT!\n")
        self.info = self.link_user_name_to_password[self.user_name]
        self.write_on_file(self.link_user_name_to_password)
        self.write_on_file(self.id_to_usr, self.file_path_bank)
        if proceed_to_login:
            self.log_in(False, True)

    def log_in(self, just_started=True, had_to_go_to_sign_up=False):
        print("Logging in...")
        name = self.ask_for_user_name()
        if name not in self.link_user_name_to_password:
            not_exist = input("User not registered!\nProceed to sign up (Y/n)?\n#").lower()
            if not_exist == 'y':
                self.sign_up(True)
            else:
                ex()

        if not had_to_go_to_sign_up or just_started:
            self.password = self.ask_for_password()
            if self.link_user_name_to_password[name]['password'] == self.password:
                if self.confirm_password():
                    self.user_name = name
                    self.balance = self.link_user_name_to_password[name]['balance']
                    self.random_pin = self.link_user_name_to_password[name]['random_pin']
                    self.access_level = self.link_user_name_to_password[name]['access_level']
                    self.id = self.link_user_name_to_password[name]['id']
                    self.load_contact_list()
                    self.info = self.link_user_name_to_password[self.user_name]
                else:
                    ex("Wrong password")
            else:
                ex("Wrong password")

'''TESTS'''

while True:
    erase_database = input("Do you want to erase the Database? (Y/n)\n#").lower()
    if erase_database == 'y':
        DataBase.erase_db()
        print("Database erased!\n")
    else:
        pass

    mode = input("\nDo you want to sign up or log in?\n1 - sign up;\n2 - log in;\n#")
    while mode not in ["1", "2"]:
        mode = input("Invalid input!\n#")

    if mode == '1':
        a1 = (DataBase().sign_up())
        ex()
    if mode == '2':
        a1 = DataBase()
        a1.log_in()
        current_menu = input("What do you want to do?\nex - exit;\n1 - transfer;\n2 - check info;\n3 - change password;\n4 - add transfer contact.\n#")
        while current_menu not in ["ex", "1", "2", "3", "4"]:
            current_menu = input("Invalid input!\n#")

        match current_menu:
            case "ex":
                ex("Exiting...")

            case "1":
                a1.transfer()

            case "2":
                if a1.access_level == 'user':
                    print(f"User name: {a1.user_name}\nBalance: {a1.balance}\nID: {a1.id}\nContacts: {', '.join(a1.id_to_usr[i] for i in a1.id_contact_list)}")
                elif a1.access_level == 'admin':
                    print(a1.info)

            case "3":
                a1.change_password()

            case "4":
                a1.add_contact()
