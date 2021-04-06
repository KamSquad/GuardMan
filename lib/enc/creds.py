import hashlib
import random
import uuid


def gen_md5(string):
    """
    Get md5 string
    :param string: target string
    :return: md5 string
    """
    byte_string = string.encode('utf-8')
    md5 = hashlib.md5(byte_string).hexdigest()
    return md5


def generate_salt(salt_len=6):
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(salt_len):
        chars.append(random.choice(alphabet))
    return "".join(chars)


def gen_uid():
    return str(uuid.uuid4())
