import random
import string

from typing import List

#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))



#make a fuction that return a random int between 1 and 1000
def random_int() -> int:
    return random.randint(1,1000)
