#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch(os=False)

import pprint
pp = pprint.PrettyPrinter(indent=2)

import logging
log = logging.getLogger(__name__)

from qbittorrent import Client
import subprocess
import time
import os
import psutil

fastcopy_cmd = [
    'fastcopy.exe',
    '/cmd=move',
    '/estimate',
    '/acl=FALSE',
    '/stream=FALSE',
    '/reparse=FALSE',
    '/verify=FALSE',
    '/recreate',
    '/error_stop=FALSE',
    '/no_ui',
    '/balloon=FALSE',
#    '"somefile"',
#    '/to="target"',
]

DST = u'D:\\'


def get_fastcopy_cmd(src, dst):

    return fastcopy_cmd + src + ['/to={}'.format(dst)]

def get_file_path(infohash, qb):

    # directory
    path = qb.get_torrent(infohash).get('save_path', '')

    # sub directory or filename
    files = qb.get_torrent_files(infohash)
    path += os.path.split(files[0]['name'])[0]

    # file
    if path.endswith(os.sep):
        path += files[0]['name']
    
    return path

def move_storage(infohash_list, qb):

    paths = []
    for infohash in infohash_list:
        path = get_file_path(infohash, qb)
        log.warning("move {} from {} to {}".format(infohash, path, DST))
        paths.append(path)

    #log.warning(get_fastcopy_cmd(path, DST))
    subprocess.call(get_fastcopy_cmd(paths, DST))
    pids = [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if 'FastCopy' in p.info['name']]

    # wait for FastCopy finish
    for pid in pids:
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue

        while True:
            try:
                time.sleep(5)
                process.wait(0)
            except psutil.TimeoutExpired:
                #log.warning("Timeout")
                continue
            except:
                break
            else:
                break

    # delete the torrent for qbittorrent
    time.sleep(1)
    qb.delete(infohash_list)

def check_if_torrent_finish(torrents, pool, qb):

    if torrents is None:
        return

    l = []
    for infohash, torrent in torrents.items():
        # check status
        # This means torrent is finished and paused
        #log.warning("{} found.".format(infohash))
        if 'pausedUP' == torrent.get('state'):
            log.warning("{} finished.".format(infohash))
            # add a job to FastCopy
            #pool.spawn_n(move_storage, infohash, qb)
            l.append(infohash)
            pass
    if l:
        pool.spawn_n(move_storage, l, qb)
    pass

def main():

    qb = Client('http://127.0.0.1:8080')
    qb.login()


    pool = eventlet.GreenPool(1)
    # Get Data
    rid = 0
    while True:
        log.warning(time.asctime(time.localtime()))
        
        try:
            data = qb.sync(rid)
            rid = data['rid']
            #pp.pprint(data.get('torrents'))
            check_if_torrent_finish(data.get('torrents'), pool, qb)
        except KeyboardInterrupt:
            break
        except:
            qb.login()
            rid = 0
            continue

        time.sleep(5 * 60)

    pass


if __name__ == '__main__':
    main()
