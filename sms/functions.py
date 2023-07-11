import random
import string

def generate_otp(length : int = 5) -> str:
    length = length or 5
    otp = ''.join(random.choices(string.digits, k=length))
    return otp



def send_otp(phone_number: str, otp: str) -> bool: 
    pass
    # send otp with getsms api
    
