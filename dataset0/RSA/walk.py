import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hashlib

private_keys_arr = []
encrypted_message_arr = []
decrypted_message_arr = []
messages_arr = []
plain_messages_arr = []
aes_plaintext_md5 = '0d3a08eaad826c46a123adbab833118e'
plain_master_message_md5 = '93a9155a61c73187dba8ddc4e5361c12'
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
        #print(i,': ',decrypted_message_arr[i])

    #print(i,': ' ,hashed.hexdigest(),'\t',aes_plaintext_md5)

##########################################################################
    #Messages 


# from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
# from cryptography.hazmat.backends import default_backend


# os.chdir('../messages')
# my_dir = os.getcwd()

# iv = b'0000000000000000'
# backend = default_backend()
# #key = 'kvlgxlzhsxedqfgbxxftfzjpghkxghbm'
# #cipher = AES.new(key, AES.MODE_CBC, iv)
# #plaintext = cipher.decrypt(read_message) 

# for dir, sub, files in os.walk(my_dir):
    
    
    
#     for f in files:
#         with open(f, 'rb') as key_file:
#             read_message = key_file.read()
#             plain_messages_arr.append(read_message)
        
        
# for i in range(len(plain_messages_arr)):
#     #print(plain_messages_arr[i])
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
#     decryptor = cipher.decryptor()
#     d_msg = decryptor.update(plain_messages_arr[i]) + decryptor.finalize() 
#     hashed = hashlib.md5(d_msg)
#         #print(d_msg) # see how many files
#     if hashed.hexdigest() == plain_master_message_md5:
#         print(i,': ',d_msg)
#         exit


os.chdir('../messages')
my_dir = os.getcwd()

read_message_arr = []

for dir, sub, files in os.walk(my_dir):
        
    for f in files:
        with open(f, 'rb') as key_file:
            read_message = key_file.read()
        read_message_arr.append(read_message)

print(key)        
print(len(read_message_arr)) # see how many files


for i in range(len(read_message_arr)):
    iv = 16 * '\x00'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(read_message_arr[i])
    plain_messages_arr.append(plaintext)
        
for i in range(len(plain_messages_arr)):
    hashed = hashlib.md5(plain_messages_arr[i])
    if hashed.hexdigest() == plain_master_message_md5:
        print(plain_messages_arr[i])
        
#print(plain_messages_arr)