import re
import pymp
import time

FILES = ('shakespeare1.txt', 'shakespeare2.txt', 'shakespeare3.txt',
        'shakespeare4.txt', 'shakespeare5.txt', 'shakespeare6.txt',
        'shakespeare7.txt' ,'shakespeare8.txt')

WORDS = ('hate', 'love', 'death', 'night', 'sleep', 'time', 'henry', 'hamlet',
        'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart', 'honest')

def words_in_file(word, file):
    count = 0
    with open(file, 'r') as f:
        for line in f:
            count += len(re.findall(word, line, re.IGNORECASE))
    return count

def main(thread_num = 1):
    global_result = pymp.shared.dict()
    for word in WORDS:
        global_result[word] = 0

    with pymp.Parallel(thread_num) as p:
        #splitting
        local_result = dict()
        for word in WORDS:
            local_result[word] = 0

        #mapping
        for i in p.range(len(FILES)):
            for word in WORDS:
                local_result[word] += words_in_file(word, FILES[i])

        #shuffling
        lock = p.lock
        for word in WORDS:
            lock.acquire()
            global_result[word] += local_result[word]
            lock.release()

    print(global_result)



for i in [1,2,3,4,5,6,7,8]:
    time1 = time.time()
    main(i)
    time2 = time.time()
    print('duration:', time2 - time1)
    print('thread_num:', i)
