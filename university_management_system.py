import os
from university import University

if __name__ == "__main__":
    stevens = University(os.path.dirname(os.path.abspath(__file__)))
    print(stevens)