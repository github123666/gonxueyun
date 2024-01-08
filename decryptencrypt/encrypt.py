from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding

key = '23DbtQHR2UMbH6mJ'


def aes_encrypt(data) -> str:
    """
    :param data:
    :return: AES encrypt
    """
    encrypt_type = AESECBPKCS5Padding(key, "hex")
    text_encrypt = encrypt_type.encrypt(str(data))
    return text_encrypt

if __name__ == '__main__':
    print(aes_encrypt('11111'))
