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
    print(aes_decrypt("23bd07ced818b143fa46532b88c27ee427353ad3ec862f4a83a4038f2fe4a68ea70aa3c2b8feca27d4a6b2a66f4b01a62072bc87064abe93b7898e11cd52a73e0e403a48589ff1de1c216806e45cc1d799e86231b4f07b2857b97762627fc6361925be1e316a7cbc459b998e26f6117a9007ff0b3319b17992fdafa5c0d40ea288d4077f98807139f743223a836efc5393581b0c9568a46e312ee1430f7f84df62a3059504e7b6cba002e7d241b7b2693a8dfe8658ff83921eecf5536eae7cec799dcb6c58f1640eccc06da354e7206780d1b523c798bde40ea17662ae2eaacd485474c9c8ae49f8f83a5ba8e7a911e1aaddb145b9837ea45751947f57374ca98f1912d852a13020733afb4a3f0a32665881b6f9abcfe28c575021671337780303c8794828024a9c5829835b7a3c6f536677c439d719e589a849187c06f37c1e150d5c4e7dff106fb2f7b7b4a09f8603a23957e3d6233e37dc9f1e24f438093a4f940f702387a64f31e207c6bd275bdee2140e6972ea8b44aca759ec01a83a9bdb1151c0dfff8d12fc1446575e2910c7107542f39cdbfdee67ab588744f870b0ca9ca017036133f36c73ca850a90c32c5e2d45caf250935db194e93137a0ba2fa4de4cd1bbc2d4865ee6e4691b92afe2bcf3aa1474c9496bb40ca1d1863fa2d8a8364acfe689023333d03cedddd4453696088725c5b5499cd96af035234f03d2d063694e7b356e0fff041d77d1d0cfa4c4cef9fabc4db820f59a3c0a739affb599dc58e4d38b051ae9a9a53e61d54336d10df90336dcf2b0d7f3b1fb8eec33a755a7d05da8a90c4abcbb2f5f76f2fb75d1f04c2398392fb0c67c617fd9b4f621d2d34b81185ae1259836a56af652bb73ff3e6cfea6389716743beb15c9048e49631511cc83a503b71150e69492c438383f57a2101c364cf23a3bf5a85f03d0afac5f725daf36fb59f5858bf07321422f54cd17ae06d3a19b8ab79a960bc81f22a1b6df903036ec7a96977c7229d8d349f9d82c8493b598bd3bae09dbe202c4d71de26081e53abe0895a734196312b5b0ec2e31cd44c73f1f4d7cf2a6f77c4c67eda3e6f0f3b9264ad6cbbc5d04338061cb6dd85fb9aa9b9b99d77293bc6ac7b19a2177c532f0071f8638f74959374c0afb474bd9051f28b437735db8532edfe7c1bc6e8e9304c9f439975ba91e1e4a88c8ba183b641f94ba1576471f06385f6e1f9127242b83d2d39cee356225a7ce1318891d4c167b2d6363ea6a6e6dcb1945d667f3bbb297a18ab303034bbf70a994620a1446463e4f599813e23b5ffa45e2f087f459cf91b0cc96917ce7fc33e17380aadba3e21710e50bba6c71970f25e2ef94633107cc56575a33572a114caceb979c807a0770053b35680d0a7cd292708fcfafd748abd36cd1b135729d81be97483031276eeab5af4b8665d157c179c434c2165bbb0a513e79510dcd9ab1f6463b4a4feaee461609125478d47aab49d5304bff753a3ee271f6b40a60f7a368d8030b9319680dfcd92038d1e9dcb71021093f2dbbb12314b73a4a11d09656104a7723556e310de5d9e4624955ebd49916ce7862c6396bd0c195a6f15dc47233dc8a9c11a1efb4019858eabe3b002c2c64ca4799d48cb5010cec3344fdba29a5248ce075dfb8aa985272712ac0d5b5e7a38a4c89f153ef3fca7cb26ab5aaf75fec49a4c62ca126896301a681e03c94c87cec1f565690d0ccd54cc077269e3e70125d5f7cf113b1e436685b1cd37c79dc23db003b44aa012b4d9832e357314b832baab8f7c368ee67d8938c4a7b3680ffcb4f84ecbaaa543b56a08c0262d5d5d6590e1738145a137460e5f0f4678e65aedf1a4477c1e093d308bf25be58d7a516d56cac14e39b2542eb150ed9989e6a6caa910fc3cd2131c00f892464549a16da67"))
