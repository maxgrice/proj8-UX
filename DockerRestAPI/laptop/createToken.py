from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
import time

def generate_auth_token(secret,user_id,expiration):
   s = Serializer(secret, expires_in=expiration)
   # pass index of user
   return s.dumps(user_id) # hashes with given user id

def verify_auth_token(token,secret):
    s = Serializer(secret) # WHAT IS SERIALIZER?
    try:
        data = s.loads(token) # Decodes the hash
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    return True