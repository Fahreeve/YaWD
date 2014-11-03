YaWD: A YandexWebDAV Client in Python
=====================================

Features
--------

* Basic authentication
* Creating directories, removing directories and files
* Uploading and downloading files
* Directory listing
* Copying and moving
* Publish files and folders

Installation
------------



Quick Start
-----------

    import YaWD
    # authorization
    ya = YaWD.connect(username='myuser', password='mypass')
    # or (in developing)
    ya = YaWD.connect(token='ya.token')
    
    # Do some stuff:
    ya.mkdir('some_dir')
    ya.rmdir('another_dir')
    ya.download('remote/path/to/file', 'local/target/file')
    ya.upload('local/path/to/file', 'remote/target/file')

Client object API
-----------------

    cd(path)
    ls(path=None)
    exists(remote_path)
    mkdir(path, safe=False)
    mkdirs(path)
    rmdir(path, safe=False)
    delete(file_path)
    upload(local_path_or_fileobj, remote_path)
    download(remote_path, local_path_or_fileobj)
    disk_free('bytes')  #size = "bytes", "kilo", "mega", "giga", "tera"
    disk_busy('bytes')
    publish(remote_path)
    unpublish(remote_path)
    ispublish(remote_path)
    getlogin() #for OAuth authorization
    copy(from_remote_path, to_remote_path)
    move(from_remote_path, to_remote_path)

