import string, secrets, os
from PIL import Image

def create_uid(prefix = '') -> str : 
    uid_str = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(9)))
    return prefix+uid_str

def is_valid_square_img(img_file) -> bool: 
    img = Image.open(img_file)
    print(img.size)
    pass
