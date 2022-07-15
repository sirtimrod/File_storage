# File storage API


This project allows you to upload, download, and delete files from local storage via a web API


### Start from docker-compose
```bash
mkdir ~/File_storage && cd ~/File_storage
https://github.com/sirtimrod/File_storage.git file_storage
cd file_storage
docker-compose up -d
# Copy this URl to browser: http://127.0.0.1:5000/
docker-compose down
```

### Start from source code:
```bash
# Create project directory
mkdir ~/File_storage && cd ~/File_storage
https://github.com/sirtimrod/File_storage.git file_storage
python3 -m venv venv
source venv/bin/activate && cd file_storage
pip install -r  requirements.txt
python3 start.py
```

### Query examples:

```text
Upload file
http://username:password@127.0.0.1:5000/api/upload
```
```json
{
    "file_hash": "<md5_hash>"
}
```

```text
Download file
http://username:password@127.0.0.1:5000/api/upload/download/<file_hash>
```

```text
Delete file
http://username:password@127.0.0.1:5000/api/upload/delete/<file_hash>
```
```json
{
    "message": "File deleted"
}
```