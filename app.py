import os
from university import University

if __name__ == "__main__":
    try:
        stevens = University(os.path.dirname(os.path.abspath(__file__)), ('\t', True), ('\t', True), ('\t', True), ('\t', True))
        print(stevens)

    except (KeyError, ValueError) as e:
        print("Bad data encountered.\n" + (e))
    except FileNotFoundError as e:
        print('Wrong folder path or missing files.\n' + str(e))