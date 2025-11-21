# # -*- coding: utf-8 -*-

# """
#     Module with useful lambdas functions/one-liners.

#     Created:  Dmitrii Gusev, 29.07.2025
#     Modified: Dmitrii Gusev, 21.11.2025
# """

# from pathlib import Path

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

# # convert python object to the human-readable JSON
# pretty_json = lambda obj: __import__('json').dumps(obj, ensure_ascii=False, indent=2)

# # get all files with the .py extebsion recursively
# files = list(Path('.').rglob('*.py'))

# # show all env variables sorted by name:
# # print('\n'.join(f'{k}={v}' for k, v in sorted(os.environ.items())))

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
