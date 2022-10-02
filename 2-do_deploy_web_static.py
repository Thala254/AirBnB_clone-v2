#!/usr/bin/python3
'''fabric script to distribute an archive to my web servers'''

from fabric.api import put, run, env
from os.path import exists


env.hosts = ['44.210.86.178', '44.200.174.223']


def do_deploy(archive_path):
    '''distributes an archive to my web servers'''
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
