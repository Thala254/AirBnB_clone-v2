#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to my web servers"""
from fabric.api import run, put, local, env
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['44.210.86.178', '44.200.174.223']


def do_pack():
    """generates an archive for web_static folder"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {filename} web_static")
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
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
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to my web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
