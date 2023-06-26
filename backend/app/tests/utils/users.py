import random
import string
from pydantic import EmailStr

def random_name_user() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=6))

def random_pasword_user() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

def random_email_user() -> EmailStr | str:
    return f"{random_name_user()}@{random_name_user()}.com"

def random_int_user() -> int:
    return random.randint(1,1000)

#make a radom password of a 10 characters
def random_password() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

