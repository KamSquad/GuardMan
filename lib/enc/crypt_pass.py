import random
import string
import base64
import sys

from lib import config

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

try:
    conf = config.JsonConfig('./config.json')
except:
    conf = config.JsonConfig('../config.json')
crypt_key = conf.value['crypt']['init_key']
key_len = conf.value['crypt']['key_len']


def get_full_c_key():
    random.seed(crypt_key)
    letters = string.ascii_lowercase
    full_seed = ''.join(random.choice(letters) for i in range(key_len)).encode('utf-8')
    return full_seed


def encrypt_password(source, encode=True):
    source = source.encode('utf-8')
    key = get_full_c_key()
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    iv = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = iv + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data


def decrypt_password(source, decode=True):
    key = get_full_c_key()
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    iv = source[:AES.block_size]  # extract the IV from the beginning
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    data = decrypter.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding].decode('utf-8')  # remove the padding


if __name__ == '__main__':
    print('Test started..')
    full_key = get_full_c_key()
    print('key={key}\n'.format(key=full_key))

    if sys.argv[1] == 'test_crypt':
        for i in range(5):
            clr_str = 'cr'
            enc = encrypt_password(clr_str)
            print('clear: {cl}\tcrypted: {cr}\tdecrypted: {dcr}'.format(cl=clr_str,
                                                                        cr=enc,
                                                                        dcr=decrypt_password(enc)))

        print('\n')

        enc = '05J2JqYzGRG/bYgD7dQp470e2lWVyUHSLuRct+ioAIA='
        print('test_crypt:', enc, decrypt_password(enc))
