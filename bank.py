import hashlib
import json
from getpass import getpass

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = self._encrypt_password(password)
        self.balance = 0.0

    def _encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self._encrypt_password(password) == self.password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def save_accounts(self):
        with open('accounts.json', 'w') as f:
            json.dump({k: v.__dict__ for k, v in self.accounts.items()}, f)

    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as f:
                accounts = json.load(f)
                for username, data in accounts.items():
                    account = Account(username, data['password'])
                    account.balance = data['balance']
                    self.accounts[username] = account
        except FileNotFoundError:
            self.accounts = {}

    def create_account(self, username, password):
        if username in self.accounts:
            raise Exception("Account already exists")
        self.accounts[username] = Account(username, password)
        self.save_accounts()

    def authenticate(self, username, password):
        if username in self.accounts and self.accounts[username].check_password(password):
            return True
        return False

    def get_account(self, username):
        return self.accounts.get(username)

def main():
    bank = Bank()
    action = input("Actions: create, login, exit: ")
    while action != 'exit':
        if action == 'create':
            username = input("Choose a username: ")
            password = getpass("Choose a password: ")
            try:
                bank.create_account(username, password)
                print("Account created successfully!")
            except Exception as e:
                print(str(e))
        elif action == 'login':
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            if bank.authenticate(username, password):
                print("Login successful!")
                account = bank.get_account(username)
                while True:
                    action = input("Available actions: deposit, withdraw, balance, logout: ")
                    if action == 'logout':
                        break
                    elif action == 'deposit':
                        amount = float(input("Amount to deposit: "))
                        if account.deposit(amount):
                            print(f"Deposited ${amount:.2f}")
                    elif action == 'withdraw':
                        amount = float(input("Amount to withdraw: "))
                        if account.withdraw(amount):
                            print(f"Withdrew ${amount:.2f}")
                    elif action == 'balance':
                        print(f"Current balance: ${account.get_balance():.2f}")
            else:
                print("Invalid login credentials")
        action = input("Actions: create, login, exit: ")

    bank.save_accounts()

if __name__ == "__main__":
    main()
