import random
import json
import tempfile
import os

from cryptography.fernet import Fernet


def add_account():
    acc_name = input("Account Name: ").lower()
    upass = input("Password: ").lower()

    acc_info = {
        "an": str(acc_name),
        "up": str(upass)
    }

    with open('accounts.json', 'r') as f:
        data = json.loads(f.read())
        data.update({random.randrange(10000):acc_info})
    
    with open('accounts.json', 'w') as f:
        insert_data = f.write(json.dumps(data, indent=4))


def validate_account(acc_name, upass):

    with open('accounts.json', 'r') as f:
        data = json.loads(f.read())

    for aid, account in data.items():

        if account['an'] == acc_name and account['up'] == upass:
            valid = (1, aid)
            break
        else:
            valid = (0)

    return valid


def menu(aid):

    while True:
        print("press v - View\npress a - Add\npress d - Delete\npress q - Quit")
        menu_val = input("Select from the following option:")
        
        if menu_val == 'v': #view list of password
            print(aid)

        elif menu_val == 'a': #add password to the list
            username = input("Add username: ")
            password = input("Add password: ")

            key = Fernet.generate_key()
            encode = Fernet(key)

            data_set = [username, password]

            path = 'tmp/' + str(aid) 

            if(os.path.isfile(path)):
                with open(path, 'r') as f:
                    enc_data = f.read()
                    # data = encode.decrypt(bytes(enc_data, 'utf-8'))

                    print(encode.key())

            else:
                with open(path, 'w') as f:
                    f.write(str(encode.encrypt(bytes(str(data_set), 'utf-8'))))
                print("successfully added!")

        elif menu_val == 'd': #delete password to the list
            pass

        elif menu_val == 'q': #quit current transaction
            break

        else:
            continue




# Main password manager code
def main():
    while True:
        is_existing = input("Do you have existing Account? (y/n) and 'q' to quit:").lower()

        if is_existing == 'y':

            while True:
                acc_name = input("Account Name: ").lower()
                upass = input("Password: ").lower()

                [status, aid] = validate_account(acc_name, upass)
                
                if status == 1:
                    menu(aid)
                    break
                else:
                    print('invalid')

        elif is_existing == 'n':
            add_account()
            print('please add user.')
        elif is_existing == 'q':
            break
        else:
            continue


# token = f.encrypt(b'Sample test data to encrypt')
# print(token)
# print(f.decrypt(token))


main()