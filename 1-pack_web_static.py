#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder
"""
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """
        generates an archive for web_static folder
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {filename} web_static")
        return filename
    except Exception:
        return None
