#!/usr/bin/python3
"""
creates and distributes an archive to your web servers
fab -f 3-deploy_web_static.py deploy -i ssh-key -u ubuntu
"""

from datetime import datetime
from os.path import isdir, isfile
from fabric.api import put, run, env, local, runs_once

env.hosts = ['44.210.86.178', '44.200.174.223']


@runs_once
def do_pack():
    """
    making an archive on web_static folder
    """
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{dt}.tgz"
    if isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local(f"tar -cvzf {file} web_static").failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, f"/tmp/{file}").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/"
           ).failed is True:
        return False
    if run(f"rm /tmp/{file}").failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)
           ).failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static"
           ).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{name}/ /data/web_static/current"
           ).failed is True:
        return False
    return True


def deploy():
    """
    Create and distribute an archive to a web server
    """
    file = do_pack()
    return do_deploy(file) if file else False
