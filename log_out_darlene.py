# Darlene Nguyen
# Last update: Nov 12, 2024

import sys

def LogOut():
    argument = input("Do you want to log out? Y/N\n").upper() # handle case-sensitive
    if argument == 'Y':
        sys.exit("You have successfully logged out.")
    elif argument == 'N':
        return True
    else:
        raise Exception("Invalid input. Please try again")
