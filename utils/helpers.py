import string, secrets, os

def create_uid(prefix = ''):
    uid_str = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(9)))
    return prefix+uid_str


