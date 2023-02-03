import rsa


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(2048)
    # print("in generate ",publicKey.value)

    with open("keys/publicKey.pem", "wb") as p:
        p.write(publicKey.save_pkcs1("PEM"))
    with open("keys/privateKey.pem", "wb") as p:
        p.write(privateKey.save_pkcs1("PEM"))


def loadKeys():
    with open("keys/publicKey.pem", "rb") as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open("keys/privateKey.pem", "rb") as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


def encrypt(message, key):
    mes = message.encode("utf-8")
    return rsa.encrypt(mes, key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode("utf-8")
    except:
        return False


# def sign(message, key):
#     return rsa.sign(message, key, "SHA-1")


def verify(message, signature, key):
    try:
        return (
            rsa.verify(
                message,
                signature,
                key,
            )
            == "SHA-1"
        )
    except:
        return False


# publicKey, privateKey = generateKeys()
# message = "kkkkkkkkkkkkkkkkvisit(Reason.Complaint,Corona,prescription([medication(50mg, [Morning, Evening]),],[doctor john, doctor ay haga],[2022/06/02 Saturday, 2022/06/03 Sunday],[pcr],),readings, 12345,Maria,)"
# ciphertext = encrypt(message, publicKey)
# signature = sign(message, privateKey)
# text = decrypt(ciphertext, privateKey).decode("utf-8")
# print(f"Cipher text: {ciphertext}")
# print(f"decrypted text: {text}")


# if text:
#     print(f"Message text: {message}")
# else:
#     print(f"Unable to decrypt the message.")
# if verify(text, signature, publicKey):
#     print("Successfully verified signature")
# else:
#     print("The message signature could not be verified")
