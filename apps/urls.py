from apps.view import FileStorageAPI


def register_urls(api):
    api.add_resource(FileStorageAPI,
            "/api/upload",   
            "/api/download/<hash>",
            "/api/delete/<hash>"
        )
