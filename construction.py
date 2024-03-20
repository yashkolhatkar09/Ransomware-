import os
from cryptography.fernet import Fernet

# first find all the files in the folder
passkey = input("Enter Your PassKey : ")


if (passkey == "Yash is the Best Programmer in the World"):
    fileslist = []

    for files in os.listdir():
        if (files == "destruction.py" or files == "Key.key" or files == "construction.py"):
            continue
        if (os.path.isfile(files)):
            fileslist.append(files)

    with open("Key.key", "rb") as key:
        key = key.read()

    with open("Key.key", "wb") as thekey:
        thekey.write(key)

    for files in fileslist:
        with open(files, "rb") as thefile:
            contents = thefile.read()
        dec_contents = Fernet(key).decrypt(contents)

        with open(files, "wb") as thefile:
            thefile.write(dec_contents)

else:
    print("Plz Make Yash Happy to Acess The PassKey")
