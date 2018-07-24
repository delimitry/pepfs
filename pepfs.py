#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import json
import logging
import os
import re
import requests
import sys
import time
from errno import ENOENT
from fuse import FUSE, FuseOSError, LoggingMixIn, Operations
from stat import S_IFDIR, S_IFREG

# use logging
logging.basicConfig(level=logging.DEBUG)

# github repository with all the latest versions of PEPs
PEPS_URL = 'http://api.github.com/repos/python/peps/contents/'


def get_peps():
    """Get PEPs from github repository"""
    response = requests.get(PEPS_URL)
    repo_files = json.loads(response.text)
    peps = {}
    for repo_file in repo_files:
        name = repo_file['name']
        # find all PEP files
        if re.match(r'pep-\d+\.txt', name):
            url = repo_file['download_url']
            size = repo_file['size']
            peps[name] = {
                'url': url,
                'size': size,
            }
    return peps


def get_data_from_url(url, timeout=10):
    """Get data from URL"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.text
    except requests.exceptions.RequestException as ex:
        logging.error(ex)


class PEPFS(LoggingMixIn, Operations):
    """PEP FUSE filesystem"""

    def __init__(self):
        # get all PEPs
        self.peps_urls = get_peps()
        # use for caching PEPs data
        self.peps_data = {}
        for pep in self.peps_urls:
            self.peps_data[pep] = None

    def getattr(self, path, fh=None):
        """Update files' attributes"""
        now = time.time()
        if path == '/':
            # calculate dir size
            dir_size = 0
            for pep in self.peps_urls:
                if self.peps_data[pep]:
                    dir_size += len(self.peps_data[pep])
                else:
                    dir_size += self.peps_urls[pep]['size']
            return {
                'st_atime': now,
                'st_ctime': now,
                'st_mtime': now,
                'st_mode': S_IFDIR | 0o755,
                'st_nlink': 2,
                'st_size': dir_size,
            }
        else:
            size = 0
            name = os.path.basename(path)
            # handle other files
            if name not in self.peps_data:
                raise FuseOSError(ENOENT)
            # set files size
            if self.peps_data[name]:
                size = len(self.peps_data[name])
            else:
                size = self.peps_urls[name]['size']
            return {
                'st_atime': now,
                'st_ctime': now,
                'st_mtime': now,
                'st_mode': S_IFREG | 0o644,
                'st_nlink': 1,
                'st_size': size,
            }

    def read(self, path, size, offset, fh):
        """Read file"""
        name = os.path.basename(path)
        data = self.peps_data[name]
        if data is None:
            # if file is not in cache - download it
            url = self.peps_urls[name]['url']
            data = get_data_from_url(url)
            self.peps_data[name] = data
        return data.encode('utf-8')[offset:offset + size]

    def readdir(self, path, fh):
        """Return all files in mountpoint dir"""
        files = ['.', '..']
        return files + sorted(self.peps_data.keys())


def main():
    if len(sys.argv) != 2:
        print('usage: {} <mountpoint>'.format(sys.argv[0]))
        exit(1)
    # make mountpoint dir if not exists
    mountpoint = sys.argv[1]
    if not os.path.isdir(mountpoint):
        os.makedirs(mountpoint)
    # init FUSE
    FUSE(PEPFS(), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    main()
