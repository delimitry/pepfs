# PEPFS
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/delimitry/pepfs/blob/master/LICENSE)

Description:
------------

A simple read-only FUSE filesystem where files are CPython PEPs.  
To build FUSE filesystem a `fusepy` module was used.

Usage:
------
The usage of `pepfs.py` is very simple:
```
usage: pepfs.py <mountpoint>
```

Example:
```
pepfs.py /tmp/pepfs/
```

The `mount` command will show just mounted FUSE filesystem:
```
...
PEPFS on /tmp/pepfs type fuse (rw,nosuid,nodev,relatime,user_id=1000,group_id=1000)
...
```

Now you can see all PEPs as the files in `/tmp/pepfs/` directory:
```
ls -la /tmp/pepfs/
total 4
drwxr-xr-x  2 root root 6943251 Jul 25 00:07 .
drwxrwxrwt 35 root root    4096 Jul 25 00:07 ..
-rw-r--r--  1 root root   29582 Jul 25 00:07 pep-0001.txt
-rw-r--r--  1 root root    8214 Jul 25 00:07 pep-0002.txt
-rw-r--r--  1 root root    2229 Jul 25 00:07 pep-0003.txt
-rw-r--r--  1 root root   11885 Jul 25 00:07 pep-0004.txt
-rw-r--r--  1 root root    3043 Jul 25 00:07 pep-0005.txt
-rw-r--r--  1 root root    8174 Jul 25 00:07 pep-0006.txt
-rw-r--r--  1 root root    7727 Jul 25 00:07 pep-0007.txt
...
-rw-r--r--  1 root root   81947 Jul 25 00:07 pep-3333.txt
```

License:
--------
Released under [The MIT License](https://github.com/delimitry/pepfs/blob/master/LICENSE).
