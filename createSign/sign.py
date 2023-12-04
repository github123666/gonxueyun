from decryptencrypt.encrypt_md5 import md5_encrypt


def create_sign(*args) -> str:
    return md5_encrypt(''.join(args) + "3478cbbc33f84bd00d75d7dfa69e0daa")


