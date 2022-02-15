import re

FILES = ('shakespeare1.txt', 'shakespeare2.txt', 'shakespeare3.txt',
        'shakespeare4.txt', 'shakespeare5.txt', 'shakespeare6.txt',
        'shakespeare7.txt' ,'shakespeare8.txt')

WORDS = ('hate', 'love', 'death', 'night', 'sleep', 'time', 'henry', 'hamlet',
        'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart', 'honest')

def words_in_file(word, file_name):
    count = 0
    with open(file_name, 'r') as file:
        for line in file:
            count += len(re.findall(word, line, re.IGNORECASE))
    return count

def main():
    result = dict()
    count = 0

    for word in WORDS:
        result[word] = 0
        for file_name in FILES:
            result[word] += words_in_file(word, file_name)

    print(result)



main()
