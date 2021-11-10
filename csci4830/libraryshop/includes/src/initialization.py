from django.core.checks.messages import ERROR
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import *
from libraryshop.models import User
from csci4830.libraryshop.models import User

import getpass


# Create administrator account. Return its object.
def create_admin(password: str):
    admin = User.objects.filter(username='admin')

    if (admin.count > 0):
        print("Admin account exists, will not create new account.")
        return

    admin = User.objects.create_superuser('admin', 'none', 'password')
    admin.save()
    return admin


def ask_password():
    ask_password.counter += 1

    if ask_password.counter == 3:
        print("Too many invalid attempts, learn to type!")
        new_password = 0
        return

    password = getpass.getpass('New password: ')
    password2 = getpass.getpass('Repeat password: ')

    if (password != password2):
        print("Passwords don't match! Try again:")
        return

    return password


def main(args):
    print("Welcome to the LibraryShop ")

    try:
        admin = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        print("Admin account not created yet. Creating admin... ")
        password = ask_password()
        create_admin('admin', 'admins@lol.hi', password)

    except MultipleObjectsReturned:
        print('/tMultiple admin accounts have been created. This means that the username is not a' +
              'unique field. Requires manual intervention, exiting.')
        exit(LookupError)

    if (admin.count() == 0):
        print("Admin account is being created...")
        admin = create_admin()
    else:
        print("The admin account has already been created.")
