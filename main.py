import string
from random import choice

def generate_short_id(num_of_chars: int):
    short_url = ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))
    return short_url

generate_short_id(8)


if __name__ == '__main__':
    print(generate_short_id(8))
