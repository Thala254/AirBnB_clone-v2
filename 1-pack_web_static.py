#!/usr/bin/python3
'''Fabric script to generate a .tgz archive'''

from fabric.api import local, runs_once
from datetime import datetime
from os.path import isdir
from os import stat


@runs_once
def do_pack():
    '''generates .tgz archive from the contents of the web_static folder'''
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = f"versions/web_static_{date}.tgz"
        print(f"Packing web_static to {filename}")
        local(f"tar -cvzf {filename} web_static")
        archive_size = stat(filename).st_size
        print(f"web_static packed: {filename} -> {archive_size} Bytes")
        return filename
    except Exception:
        return None
