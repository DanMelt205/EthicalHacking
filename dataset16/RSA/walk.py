import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib

private_keys_arr = []
encrypted_message_arr = []
decrypted_message_arr = []
messages_arr = []
plain_messages_arr = []
aes_plaintext_md5 = '289103efdd93a48578023df5f6bae09f'
plain_master_message_md5 = 'ec10d38a26c93f3fa99977fb579151d9'
key = 0

##########################################################################
    #Looping through the key pairs. Only saving private keys to the array

os.chdir('./pairs')
my_dir = os.getcwd()

for dir, sub, files in os.walk(my_dir):

    files[:] = [f for f in files if not f.startswith('public')] 

    contents = files
    contents.sort()

    for f in files:
        with open(f, 'rb') as key_file:
            private_key = RSA.importKey(key_file.read())
            #print(private_key)
            private_keys_arr.append(private_key)

#print(private_keys_arr)

#########################################################################
    #Looping through the session keys. Storing in an array

os.chdir('../session_keys')
my_dir = os.getcwd()

for dir, sub, files in os.walk(my_dir):
    
    contents = files
    contents.sort()

    for f in files:
        with open(f, 'rb') as key_file:
            encrypted_message = key_file.read()
            encrypted_message_arr.append(encrypted_message)

#print(encrypted_message_arr)

##########################################################################
    #Decrypting the message with the private key and session key

for i in range(len(private_keys_arr)):
    decrypted_message = private_keys_arr[i].decrypt(encrypted_message_arr[i])
    decrypted_message_arr.append(decrypted_message)

#print(decrypted_message_arr)


#########################################################################
    #Finding the hashed key in the decrypted message#

for i in range(len(decrypted_message_arr)):
    hashed = hashlib.md5(decrypted_message_arr[i])
    if hashed.hexdigest() == aes_plaintext_md5:
        key = decrypted_message_arr[i]
        print(i,':', decrypted_message_arr[i])

##########################################################################
    #Messages 

os.chdir('../messages')
my_dir = os.getcwd()

read_message_arr = []

for dir, sub, files in os.walk(my_dir):
        
    for f in files:
        with open(f, 'rb') as key_file:
            read_message = key_file.read()
        read_message_arr.append(read_message)

#print(key)        
#print(len(read_message_arr)) # see how many files


for i in range(len(read_message_arr)):
    iv = 16 * b'\x00'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(read_message_arr[i])
    plain_messages_arr.append(plaintext)
        
for i in range(len(plain_messages_arr)):
    hashed = hashlib.md5(plain_messages_arr[i])
    if hashed.hexdigest() == plain_master_message_md5:
        print(plain_messages_arr[i])

