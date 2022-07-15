from flask import jsonify, request, send_file, make_response, abort
from flask_restful import Resource

from config import Config
from apps.models import User, File
from apps.utils import hash_file, create_dir, save_file, check_user, delete_dir, join_path


create_dir(Config.UPLOAD_FOLDER)

class FileStorageAPI(Resource):
    
    def get(self, hash: str):
        file = File.get_file(hash)

        if not file:
            return abort(404, {"error": "File not found"})

        name = file.filename + '.' + file.extension
        path = join_path(Config.UPLOAD_FOLDER, hash[0:2], hash)

        try:
            return send_file(path, attachment_filename=name, as_attachment=True)
        except FileNotFoundError:
            return abort(404, {"error": "File not found"})

    @check_user
    def post(self):
        file = request.files['file']

        if not file:
            abort(400, {'error': 'The file was not uploaded'})

        name = request.authorization.username
        passwd = request.authorization.password
        filename, extension = file.filename.split('.')
        hash = hash_file(file)
        exist_file = File.get_file(hash)

        if exist_file:
            if User.check_file(exist_file, name, passwd):
                return abort(409, f"User '{name}' has already uploaded " 
                                  f"'{filename}.{extension}' file")
            else:
                User.append_file(exist_file, name, passwd)
                return make_response(jsonify({'file_hash': hash}), 201)

        try:
            save_file(file, hash, Config.UPLOAD_FOLDER)
        except Exception:
            return abort(400, {"error": "File upload error"})
        else:
            new_file = File.add_file(
                filename=filename, 
                extension=extension, 
                hash=hash)
            User.append_file(new_file, name, passwd)
            return make_response(jsonify({'file_hash': hash}), 201)


    @check_user
    def delete(self, hash: str):
        name = request.authorization.username
        passwd = request.authorization.password
        exist_file = File.get_file(hash)

        if not exist_file:
            abort(404, {'error': 'File not found'})

        if User.check_file(exist_file, name, passwd) == False:
            abort(400, {'error': f"User '{name}' did't upload '{hash}' file"})

        if File.check_users(hash) <= 1:
            try:
                delete_dir(hash)
                File.delete_file(hash)
                return jsonify({"message": "File deleted"})
            except FileNotFoundError:
                return abort(404, {"error": "File not found"})
        else:
            User.delete_appended_file(exist_file, name, passwd)
            return jsonify({"message": "File deleted"})
