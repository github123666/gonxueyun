import hashlib


def md5_encrypt(data):
    """
    :param data:
    :return: md5
    """
    return hashlib.md5(data.encode("utf-8")).hexdigest()


if __name__ == '__main__':
    print(md5_encrypt(''))
