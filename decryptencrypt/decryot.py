from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding

key = '23DbtQHR2UMbH6mJ'


def aes_decrypt(data) -> str:
    """
    :param data:
    :return: AES encrypt
    """
    decrypt_type = AESECBPKCS5Padding(key, "hex")
    text_decrypt = decrypt_type.decrypt(str(data))
    return text_decrypt


if __name__ == '__main__':
    print(aes_decrypt(""))
