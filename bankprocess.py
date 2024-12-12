import random
import time

import mysql
import re
import mysql.connector
import datetime


# import pandas


class User:
    def __init__(self):
        # Attributes to store user information
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bankproject"
        )
        self.surname = ""
        self.firstname = ""
        self.account_name = ""
        self.email = ""
        self.password = ""
        self.pin = ""
        self.address = ''
        self.phone = ''
        self.acc_balance = 0
        self.acc_no = get_acc_no()
        self.amount = 0
        self.transaction_type = ''
        self.date = get_formatted_date()

    def sign_up(self):
        print('\nEnter your details to sign up')
        # Getting user input
        self.surname = input('Surname: ')
        self.firstname = input('Firstname: ')
        self.account_name = input('Account Name: ')
        self.email = input('Email: ')
        is_valid_email(self.email)
        self.address = input('Address: ')

        def pin():
            while True:
                try:
                    self.pin = int(input('PIN: '))
                    if len(str(self.pin)) == 4:
                        break
                    else:
                        print('PIN must be four(4) digits.')
                except ValueError:
                    print('Your PIN must be four(4) digits.')

        pin()

        def contact():
            while True:
                try:
                    self.phone = int(input('Phone Number: '))
                    if len(str(self.phone)) >= 10:
                        break
                    else:
                        print('Your phone number should be 11 digits.')
                except ValueError:
                    print('Your phone number must consist of 11 digits.')

        contact()
        self.password = input('Password: ')
        confirm_password = input('Confirm Password: ')

        # Check if passwords match
        if self.password != confirm_password:
            print('Passwords do not match. Please restart the signup process.')
            self.sign_up()  # restart sign up if passwords don't match
        else:
            cursor = self.db.cursor()
            myquery = ("INSERT INTO clients (surname, first_name, account_name,"
                       " email, `password`, pin, phone_no, address, account_number) "
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            val = (self.surname, self.firstname, self.account_name,
                   self.email, self.password, self.pin,
                   self.phone, self.address, self.acc_no)

            try:
                cursor.execute(myquery, val)
                self.db.commit()  # Save changes to the database
                print('Loading ....')
                time.sleep(4)
                print("User signed up successfully.")
                self.login()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()

    def login(self):
        counter = 0  # Move the counter here
        while counter < 3:  # Limit attempts to 3
            print('\n\nLogin to access your dashboard')
            self.email = input("Enter Email: ")
            is_valid_email(self.email)
            self.password = input("Password: ")

            cursor = self.db.cursor()
            query = "SELECT * FROM clients WHERE email = %s AND password = %s"
            cursor.execute(query, (self.email, self.password))

            result = cursor.fetchall()
            if result:
                query = "SELECT account_name FROM clients WHERE email = %s"
                cursor.execute(query, (self.email,))
                self.account_name = cursor.fetchone()[0]
                print(f"Login successful. Welcome, {self.account_name}!")
                self.choose_account()
                break
            else:
                print("Invalid login credentials. Please try again.")
                counter += 1
                if counter == 3:
                    print("Too many failed attempts. Exiting.")
                    exit()

    def choose_account(self):
        account_type = self.select_account()
        if account_type:
            self.perform_transaction(account_type)

    def get_account_balance(self, account_type):
        cursor = self.db.cursor()
        query = f"SELECT {account_type}_balance FROM clients WHERE account_name = %s"
        cursor.execute(query, (self.account_name,))
        result = cursor.fetchall()
        return result[0][0]

    def update_account_balance(self, account_type, new_balance):
        cursor = self.db.cursor()
        sql = f"UPDATE clients SET {account_type}_balance = %s WHERE account_name = %s"
        cursor.execute(sql, (new_balance, self.account_name))
        self.db.commit()

    def select_account(self):
        print('Please choose an account\n'
              '\n1. Checking account'
              '\n2. Savings account')
        choice = input('>>> ')
        if choice == '1':
            return 'checkings'
        elif choice == '2':
            return 'savings'
        else:
            print("Invalid choice")
            return None

    def perform_transaction(self, account_type):
        self.acc_balance = self.get_account_balance(account_type)
        print(f'\t\t\t\t{str(self.account_name).upper()}'
              f'\n\nYour balance\n${self.acc_balance}')
        print('What transaction would you like to perform today?\n'
              '1. Deposit\n'
              '2. Withdraw\n'
              '3. Transfer\n'
              '4. View Transaction History')
        choice = input('>>> ')

        if choice == '1':  # Deposit
            self.transaction_type = 'Deposit'
            self.amount = int(input('Enter Amount to deposit: $'))
            if self.amount < 0:
                print('Invalid amount. The amount to deposit must be more than $0')
                self.continue_transaction()
            else:
                pass
            self.validation()
            new_balance = self.acc_balance + self.amount
            self.update_account_balance(account_type, new_balance)
            print('Loading transaction....')
            time.sleep(4)
            print(f'${self.amount} deposited. New balance is ${new_balance}.')
            self.record_transaction()
            self.continue_transaction()

        elif choice == '2':  # Withdraw
            self.transaction_type = 'Withdraw'
            self.amount = int(input('Enter Amount to withdraw: $'))
            if self.amount < 0:
                print('Invalid amount. The amount to deposit must be more than $0')
                self.continue_transaction()
            else:
                pass
            self.validation()
            new_balance = self.acc_balance - self.amount
            if new_balance < 0:
                print('Transaction failed. Insufficient balance')
                self.continue_transaction()
            else:
                pass
            self.update_account_balance(account_type, new_balance)
            print('Loading transaction....')
            time.sleep(4)
            print(f'${self.amount} Withdrawn successfully. New balance is ${new_balance}')
            self.record_transaction()
            self.continue_transaction()

        elif choice == '3':
            self.transaction_type = 'Transfer'
            input('Recipient Account:  ')
            self.amount = int(input('Enter Amount to Transfer: $'))
            if self.amount < 0:
                print('Invalid amount. The amount to deposit must be more than $0')
                self.continue_transaction()
            else:
                pass
            self.validation()
            new_balance = self.acc_balance - self.amount
            if new_balance < 0:
                print('Transaction failed. Insufficient balance')
                self.continue_transaction()

            else:
                pass
            self.update_account_balance(account_type, new_balance)
            print('Loading transaction....')
            time.sleep(4)
            print(f'${self.amount} Transferred successfully. New balance is ${new_balance}')
            self.record_transaction()
            self.continue_transaction()

        elif choice == '4':
            self.view_transaction_history()

        else:
            print("Invalid choice")

    def record_transaction(self):
        cursor = self.db.cursor()
        query = ("INSERT INTO transactions (account_name, amount, transaction_type, date) "
                 "VALUES(%s, %s, %s, %s)")
        val = (self.account_name, self.amount, self.transaction_type, self.date)
        cursor.execute(query, val)
        self.db.commit()

    def continue_transaction(self):
        choice = input('Would you like to continue\n'
                       '1. continue\n'
                       '2. Log out\n'
                       '>>> ')
        if choice == '1':
            account_type = self.select_account()
            self.perform_transaction(account_type)
        elif choice == '2':
            print(f'{self.account_name} logged out successfully '
                  f'\nThank you for banking with us we look forward to serving you in the future')
            exit()
        else:
            print('Invalid choice')
            self.continue_transaction()

    def view_transaction_history(self):
        cursor = self.db.cursor()
        query = "SELECT amount, transaction_type, date FROM transactions WHERE account_name = %s"
        cursor.execute(query, (self.account_name,))
        result = cursor.fetchall()
        header = ('AMOUNT', 'TRANSACTION', 'DATE')
        print("{:<10} {:<10} {:<10}".format(*header))
        for i in result:
            print("${:<10} {:<10} {:<10}".format(*i))

    def validation(self):
        self.pin = input('Enter Pin to continue: ')
        cursor = self.db.cursor()
        query = "SELECT * FROM clients WHERE account_name = %s AND pin = %s"
        cursor.execute(query, (self.account_name, self.pin))
        result = cursor.fetchall()
        if result:
            pass
        else:
            print('Wrong pin. Pls try again')
            self.validation()
            counter = 0
            counter += 1
            if counter == 2:
                exit()


def is_valid_email(email):
    # Regular expression for validating an Email

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # If the string matches the regex, it is a valid email

    if re.match(regex, email):
        pass
    else:
        print(f"'{email}' is an invalid email address.\n"
              f"Pls enter a valid email address eg. `abcdpeople@gmail.com`")
        email = input('Email: ')
        is_valid_email(email)


def check_status():
    print('Loading...')
    time.sleep(4)
    user = User()
    print('\nPls choose an option'
          '\n1. Login'
          '\n2. Signup'
          '\n3. Customer Care')
    ans = input('>>> ')
    if ans == '1':
        user.login()
    elif ans == '2':
        user.sign_up()
    elif ans == '3':
        print('Pls contact any of our media platforms')


def get_day_suffix(day):
    if 11 <= day <= 13:
        return 'th'
    elif day % 10 == 1:
        return 'st'
    elif day % 10 == 2:
        return 'nd'
    elif day % 10 == 3:
        return 'rd'
    else:
        return 'th'


def get_formatted_date():
    today = datetime.datetime.today()
    day = today.day
    day_suffix = get_day_suffix(day)
    return today.strftime(f'%d{day_suffix} %B, %Y')


def get_acc_no():
    number = random.randint(11232356096, 106435687199)
    # print(number)
    return number

