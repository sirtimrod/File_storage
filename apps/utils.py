import os
import hashlib
from functools import wraps
import shutil

from flask import request, Response, abort
from werkzeug.datastructures import FileStorage

from apps.models import User
from config import Config


def join_path(*args: str) -> str:
    """Creates a path"""
    
    return os.path.join(*args)

def hash_file(file: FileStorage) -> str:
    """Generates a hash of a file"""

    hasher = hashlib.md5()
    buf = file.read(65536)
    hasher.update(buf)
    return hasher.hexdigest()

def create_dir(path: str) -> str:
    """Creates a directory for a file"""

    os.makedirs(path, exist_ok=True)
    return path

def save_file(file: FileStorage, hash: str, path):
    """Saves a file on the server"""

    path = create_dir(join_path(Config.UPLOAD_FOLDER, hash[0:2]))
    file.seek(0)
    file.save(os.path.join(path, hash))

def delete_dir(hash: str):
    """Deletes the directory containing a single file"""

    path = join_path(Config.UPLOAD_FOLDER, hash[0:2])

    if len(os.listdir(path)) > 1:
        return

    shutil.rmtree(path, ignore_errors=False)

def check_user(func):
    """Authorizes the user and adds him if he does't exist"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        auth = request.authorization
        if not auth:
            return abort(401, 
                'Could not verify your access level for that URL. '
                'You have to login with proper credentials')

        name = auth.username
        passwd = auth.password
        user = User.get_user(name, passwd)
        if user:
            return func(*args, **kwargs)
        else:
            User.add_user(username=name, password=passwd)
            return func(*args, **kwargs)
    return wrapper
