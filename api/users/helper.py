import binascii
import os
import random


def generate_token(min_length=30, max_length=40):
    """ generates a pseudo random code using os.urandom and binascii.hexlify """
    # determine the length based on min_length and max_length
    length = random.randint(min_length, max_length)

    # generate the token using os.urandom and hexlify
    return binascii.hexlify(
        os.urandom(max_length)
    ).decode()[0:length]


def generate_code(length=6):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)
