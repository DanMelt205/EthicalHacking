import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib
import time

start = time.time()
private_keys_arr = []
session_keys_arr = []
decrypted_session_key_arr = []
read_message_arr = []
plain_messages_arr = []
key = 0

###########################################################################
    #Get the message hashes for comparing

with open('plain_AES_hash.md5', 'r') as aes, open('plain_master_message_hash.md5', 'r') as msg:
    aes_plaintext_md5 = aes.read()
    plain_master_message_md5 = msg.read()

##########################################################################
    #Looping through the key pairs. Only saving private keys to the array

os.chdir('RSA/pairs')
my_dir = os.getcwd()

for dir, sub, files in os.walk(my_dir):

    files[:] = [f for f in files if not f.startswith('public')] 

    contents = files
    contents.sort()

    for f in files:
        with open(f, 'rb') as key_file:
            private_key = RSA.importKey(key_file.read())
            private_keys_arr.append(private_key)


#########################################################################
    #Looping through the session keys. Storing in an array

os.chdir('../session_keys')
my_dir = os.getcwd()

for dir, sub, files in os.walk(my_dir):
    
    contents = files
    contents.sort()

    for f in files:
        with open(f, 'rb') as key_file:
            session_key = key_file.read()
            session_keys_arr.append(session_key)


##########################################################################
    #Decrypting the session key with the private key

for i in range(len(private_keys_arr)):
    decrypted_session_key = private_keys_arr[i].decrypt(session_keys_arr[i])
    decrypted_session_key_arr.append(decrypted_session_key)


#########################################################################
    #Finding the hashed key in the decrypted session key

for i in range(len(decrypted_session_key_arr)):
    hashed = hashlib.md5(decrypted_session_key_arr[i])
    if hashed.hexdigest() == aes_plaintext_md5:
        key = decrypted_session_key_arr[i]
       

##########################################################################
    #Show decrypted Message 

os.chdir('../messages')
my_dir = os.getcwd()

for dir, sub, files in os.walk(my_dir):
        
    for f in files:
        with open(f, 'rb') as key_file:
            read_message = key_file.read()
        read_message_arr.append(read_message)

##########################################################################
    #Decrypting the message with AES crypto

for i in range(len(read_message_arr)): 
    iv = 16 * b'\x00'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(read_message_arr[i])
    plain_messages_arr.append(plaintext)

##########################################################################
    #Finding the hashed message and printing the message
             
for i in range(len(plain_messages_arr)):
    hashed = hashlib.md5(plain_messages_arr[i])
    if hashed.hexdigest() == plain_master_message_md5:
        print(plain_messages_arr[i])

end = time.time()        
print(end - start)