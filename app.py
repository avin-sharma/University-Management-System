import os
from university import University

if __name__ == "__main__":
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stevens = University(current_dir, ('\t', True), ('\t', True), ('\t', True), ('\t', True), os.path.join(current_dir, 'database.db'))
        print(stevens)
    except (KeyError, ValueError) as e:
        print("Bad data encountered.\n" + (e))
    except FileNotFoundError as e:
        print('Wrong folder path or missing files.\n' + str(e))