#!/usr/bin/env bash

export MACHINE=zzz

python - << END

import os
import sys

# show current $PATH value
print(f"1 -> PATH={os.environ['PATH']}")
print(f"\n111 -> PATH={sys.path}\n")

# grab $PATH and split it
path = os.environ['PATH'].split(';')
print(f"\n\n **** -> {path}\n\n")

machine = os.environ['MACHINE']
if machine == 'zzz':
    print("It'z Z-Machine!")
else:
    print("UNKNOWN!")

# filter out empty values and normalize all paths
path = map(os.path.normpath, filter(lambda x: (len(x.strip()) > 0), path))

# remove duplicates via a dictionary
clean = dict.fromkeys(path)
# print(clean)

# combine back into one path
clean_path = ';'.join(clean.keys())

# dump to stdout
print(f"2 -> PATH={clean_path}")

os.environ['PATH'] = clean_path
print(f"\n\n3 -> PATH={os.environ['PATH']}")

END