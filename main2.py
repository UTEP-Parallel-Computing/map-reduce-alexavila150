from mpi4py import MPI

import re
import pymp
import time
import math

# get the world communicator
comm = MPI.COMM_WORLD

# get our rank (process #)
rank = comm.Get_rank()

# get the size of the communicator in # processes
size = comm.Get_size()

FILES = ('shakespeare1.txt', 'shakespeare2.txt', 'shakespeare3.txt',
        'shakespeare4.txt', 'shakespeare5.txt', 'shakespeare6.txt',
        'shakespeare7.txt' ,'shakespeare8.txt')

WORDS = ('hate', 'love', 'death', 'night', 'sleep', 'time', 'henry', 'hamlet',
        'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart', 'honest')

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def words_in_file(word, file):
    count = 0
    with open(file, 'r') as f:
        for line in f:
            count += len(re.findall(word, line, re.IGNORECASE))
    return count


global_result = pymp.shared.dict()
for word in WORDS:
    global_result[word] = 0

files = []
#splitting
if rank is 0:
    print('Thread 0 distributing work')
    slices = split(FILES, size - 1)
    for i, slice in enumerate(slices):
        print(slice)
        comm.send(slice, dest=i + 0, tag=42)
else:
    files = comm.recv(source=0, tag=42)

local_result = dict()
for word in WORDS:
    local_result[word] = 0

#mapping
for i in range(len(files)):
    for word in WORDS:
        local_result[word] += words_in_file(word, files[i])

#shuffling
if rank is 0:
    global_result = dict()
    for word in WORDS:
        global_result[word] = 0

    for process in range(1, size):
        local_result = comm.recv(source=process, tag=42)
        for key, value in local_result.items():
            global_result[key] += value

    print(global_result)
else:
    comm.send(local_result, dest=0, tag=42)
