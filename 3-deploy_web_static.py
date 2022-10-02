#!/usr/bin/python3
"""
creates and distributes an archive to your web servers
fab -f 3-deploy_web_static.py deploy -i ssh-key -u ubuntu
"""

from datetime import datetime
from os import stat
from os.path import exists, isdir
from fabric.api import put, run, env, local, runs_once

env.hosts = ['44.210.86.178', '44.200.174.223']


@runs_once
def do_pack():
    """
    generates an archive for web_static folder
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"versions/web_static_{date}.tgz"
        if isdir("versions") is False:
            local("mkdir versions")
        print(f"Packing web_static to {filename}")
        local(f"tar -cvzf {filename} web_static")
        archive_size = stat(filename).st_size
        print(f"web_static packed: {filename} -> {archive_size} Bytes")
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}')
        run(f'tar -xzf /tmp/{filename} -C {path}{no_ext}/')
        run(f'rm /tmp/{filename}')
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """
    Create and distribute an archive to a web server
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
