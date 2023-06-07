import string
import random
import argparse

def gen_random_sentence(prefix:str, length: int):
    randomized = ""
    for i in range(length):
        random_char = random.choice(string.ascii_letters)
        randomized+=random_char
    return prefix + randomized

parser = argparse.ArgumentParser()
parser.add_argument("prefix")
parser.add_argument("random_length", help="random_length",
                    type=int)
args = parser.parse_args()

_str = gen_random_sentence(prefix=args.prefix, length=args.random_length)
print(_str)

