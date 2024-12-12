import time
from datetime import datetime
import bankprocess


def greet():
    current_hr = datetime.now().hour

    if current_hr <= 11:
        print('Good morning USER')
    elif 12 <= current_hr < 17:
        print('Good afternoon USER')
    elif 17 <= current_hr <= 23:
        print('Good evening USER')
    print(f'\nWhich bank would you like to use?')
    bank = input('1. Firstbank'
                 '\n2. GTBank'
                 '\n3. Zenith Bank'
                 '\n>>> ')
    if bank == '1':
        print('Welcome to FIRSTBANK 😊'
              '\nThe Premier Bank of West Africa')
        bankprocess.check_status()
    elif bank == '2':
        print('Welcome to Guaranty Trust Bank (GTB)'
              '')
        bankprocess.check_status()
    elif bank == '3':
        print('Welcome to Zenith Bank'
              '\nA Bank In Your Own Interest')
        bankprocess.check_status()


greet()
