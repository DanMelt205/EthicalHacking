#import required modules from libraries
from Crypto.PublicKey import RSA 
import hashlib

#create function to decrypt session keys as we open them in the while loop
def decrypt(ciphertext, key):
    private_key = key
    private_key_object = RSA.importKey(private_key)
    message = private_key_object.decrypt(ciphertext) 
    return message


#nested while loops to run each session key through before moving to next private key
#code will print only two lines once the match is found.
#If no match was found, it wont print anything, to keep the window clear.

i=0
while i<150:
    z="private_key" + str(i) + ".pem"   #automatically changes key name once done with previous one
    key = open(z,'rb')
    pk = key.read()
    key.close()
    print(key)

    x=0                 #nested loop for session keys
    while x<150:
        y = "session_key" + str(x) + '.eaes' #automatically changes name #no user input necessary
        data = open(y,'rb')
        cipher_text = data.read()
        data.close()                 #close file to prevent leaking
        decrypted_mes = decrypt(cipher_text,pk)        #call decrypt function we made above
        new_hash = hashlib.md5(decrypted_mes).hexdigest();     #generate md5 hash of decrypted msg
        master = open('plain_AES_hash.md5','r') #open given md5 hash file
        old_hash = master.read() 
        if new_hash == old_hash:    #compare two hashes to verify the match
            print("you finally found a match.")  
            print("private key" + str(i) + " and session key " + str(x))
        master.close()
        x = x+1
    i=i+1
#while loop ends, revealing exactly the session key and private key that are useful for part-2


from Crypto.Cipher import AES

#decrypt function to put in the while loop since there
#are 90,000 messages

def decryption2(encrypted_message, key):
    mode = AES.MODE_CBC
    iv = 16*"\x00"
    private_key = key
    private_key_object = AES.new(private_key)
    plaintext = private_key_object.DecodeAES(encrypted_message)
    return plaintext

#use session key we found in part-1
    a = open('session_key.aes','rb') 
    key = key.read()
    a.close()

i=0
while i<90000:
    z="message" + str(i) + ".emsg"   #automatically changes message name once done with previous one
    message = open(z,'rb')
    a = message.read()
    message.close()
    text = decryption2(a,key)  #feed key to the current message
    new_hash = hashlib.md5(text).hexdigest();#generate md5 hash of decrypted msg
    master = open('plain_master_message_hash.md5','r') #open given md5 hash file
    old_hash = master.read() 
        if new_hash == old_hash:    #compare two hashes to verify the match
            print("you finally found a match.")  
            print("the correct message is: message" +str(x))
            print("The contents of the message is: " + text)
    master.close()    
    i=i+1
    
#while loop will take about 4 mins to loop through and find the right message.