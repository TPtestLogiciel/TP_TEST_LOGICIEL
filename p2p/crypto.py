import os
import sys
import hashlib

import OpenSSL
from OpenSSL import crypto
import base64

def SendKey(PublicKey):
    if os.path.exists(PublicKey):
        print(PublicKey)
        KeyFfile = open(PublicKey,mode='r')
        content = KeyFile.read()    
        #print(content)    
        KeyFile.close()
        return 1
    else:
        return -1

def SignMsg(PrivateKey):
    KeyFile = open(PrivateKey,"r")
    KeyContent = KeyFile.read()
    KeyFile.close()
    mdp = "azertyuiop"

    if KeyContent.startswith('-----BEGIN '):
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, KeyContent,mdp.encode())
    else:
        pkey = crypto.load_pkcs12(KeyContent, mdp).get_privatekey()
    print (pkey)
    data="MESSAGE A SIGNER"
    ByteData=str.encode(data)
    MsgFile = open("MsgFile.txt","wb+")
    MsgFile.write (ByteData)
    MsgFile.close()


    sign = OpenSSL.crypto.sign(pkey,ByteData,"sha256")
    signature = open("sign.sha256","wb+") #wb write byte et + pour creation file
    signature.write (sign);
    signature.close()

    #MsgFile = open("MsgFile.txt","wb+")
    #MsgFile.write (str.encode("aaaaaaaaaaaaaaaaaa"))
    #MsgFile.close()

    data_base64 = base64.b64encode(sign)
    signatureb64 = open("sign","wb+")
    signatureb64.write (data_base64);
    signatureb64.close()

def VerifSign(PublicKey):
    PublicKeyFile = open(PublicKey,"rb")
    PublicKeyContent = PublicKeyFile.read()
    PublicKeyFile.close()
    print(PublicKeyContent)

    cert = crypto.load_certificate(crypto.FILETYPE_PEM,PublicKeyContent)
    SignatureFile = open("sign.sha256","rb")
    SignatureContent = SignatureFile.read()
    SignatureFile.close()

    MsgFile = open("MsgFile.txt","rb")
    MsgContent = MsgFile.read()
    MsgFile.close()

    try:
        OpenSSL.crypto.verify(cert,SignatureContent,MsgContent,'sha256')    
        print("Verif is ok")
    except:
        print("Verif is not ok")

if(__name__ =='__main__'):
    privatekey = sys.argv[1]
    publickey = sys.argv[2]
    SignMsg(privatekey)
    VerifSign(publickey)



