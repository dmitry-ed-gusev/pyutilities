# -*- coding: utf-8 -*-

"""
Lambdas module. Contains useful lambda functions.

Created:  Dmitrii Gusev, 15.05.2026
Modified: Dmitrii Gusev, 15.05.2026
"""

import logging

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# # execute shell cmd and return output
# sh = lambda cmd: __import__('subprocess').run(cmd, shell=True, check=True, capture_output=True) \
#                                          .stdout.decode().strip()

# # read the last n strings from file (tail-like)
# tail = lambda f, n=10: list(__import__('collections').deque(open(f), maxlen=n))

# # decorator for memoizing the function call result
# memoize = lambda f: (lambda *args, _cache={}, **kwargs: _cache.setdefault((args, tuple(kwargs.items())),
#                                                                           f(*args, **kwargs)))

# # split list into n-sized chunks
# chunked = lambda lst, n: [lst[i:i+n] for i in range(0, len(lst), n)]

# # get all files with the .py extension recursively
# files = list(Path('.').rglob('*.py'))

# # read all lines from file, removing wrap line
# lines = Path('file.txt').read_text().splitlines()

# # get SHA256 code of the string
# hash = hashlib.sha256(b"your text").hexdigest()

# # quickly stop the script execution
# raise SystemExit("Done")

# # print object in the memory size
# print(sys.getsizeof(obj))

# # truncate string length with ... symbols
# s_trunc = s[:n] + '…' if len(s) > n else s

# # get file size in megabytes
# size_mb = os.path.getsize(path) / 1024**2

# # check host liveness without ping
# ok = socket.create_connection((host, port), timeout=2)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
