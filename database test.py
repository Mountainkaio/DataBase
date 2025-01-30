
from sys import exit as ex
from random import randint, choice

class DataBase:
    link_user_name_to_password = {}
    password_confirmed = False
    file_path = "db.txt"

    def __init__(self):
        self.load_from_file()
        self.user_name = ""
        self.password = ""
        self.random_pin = ''
        self.info = ''
        self.access_level = 'user'
        self.balance = 0
        # self.link_user_name_to_password[self.user_name]

    @classmethod
    def erase_db(cls):
        with open(cls.file_path, "w") as file:
            file.write("")

    @staticmethod
    def ask_for_user_name(): #will be used upon __init__; probably
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

    def confirm_password(self):
        check_password = input("Confirm your password:\n#").strip(" ").lower()
        return True if check_password == self.password else False

    def add_user(self):
        if self.confirm_password():
            self.link_user_name_to_password[self.user_name] = {'password':self.password, 'balance':self.balance, 'random_pin':self.random_pin, 'access_level':self.access_level}
            print("Registered successfully!")
        else:
            ex("Wrong password!")

    def check_user_existence(self):
        return True if self.user_name in self.link_user_name_to_password else False

    @classmethod
    def write_on_file(cls, data):
        with open(cls.file_path, "w") as file:
            file.write(str(data))

    @classmethod
    def load_from_file(cls):
        try:
            with open(cls.file_path, "r") as file:
                cls.link_user_name_to_password = eval(file.read().strip())
        except (FileNotFoundError, SyntaxError):
            cls.link_user_name_to_password = {}

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

        print(self.random_pin == ask_for_random_pin)

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
        if proceed_to_login:
            self.log_in()

    def log_in(self):
        print("Logging in...")
        just_started = True
        had_to_go_to_sign_up = False
        name = self.ask_for_user_name()
        if name not in self.link_user_name_to_password:
            not_exist = input("User not registered!\nProceed to sign up (Y/n)?\n#").lower()
            if not_exist == 'y':
                self.sign_up(True)
                had_to_go_to_sign_up = True
                just_started = False
            else:
                ex()

        if had_to_go_to_sign_up or just_started:
            self.password = self.ask_for_password()
            if self.link_user_name_to_password[name]['password'] == self.password:
                if self.confirm_password():
                    self.user_name = name
                    self.balance = self.link_user_name_to_password[name]['balance']
                    self.random_pin = self.link_user_name_to_password[name]['random_pin']
                    self.access_level = self.link_user_name_to_password[name]['access_level']
                    self.info = self.link_user_name_to_password[self.user_name]
            else:
                ex("Wrong password")

'''TESTS'''

while True:
    erase_database = input("Do you want to erase the Database? (Y/n)\n#").lower()
    if erase_database == 'y':
        DataBase.erase_db()
        print("Database erased!\n")

    mode = input("\nDo you want to sign up or log in?\n1 - sign up;\n2 - log in;\n#")
    while mode not in ["1", "2"]:
        mode = input("Invalid input!\n#")

    if mode == '1':
        a1 = (DataBase().sign_up())
        ex()
    if mode == '2':
        a1 = DataBase()
        a1.log_in()
        current_menu = input("What do you want to do?\n1 - transfer;(TODO)\n2 - check info;\n3 - change password.\n#")
        while current_menu not in ["1", "2", "3"]:
            current_menu = input("Invalid input!\n#")

        if current_menu == '1':
            pass
        if current_menu == '2':
            print(a1.info)
        if current_menu == '3':
            a1.change_password()

# print(a1.link_user_name_to_password[a1.user_name]['password'])
