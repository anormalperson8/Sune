def get(list1984):
    f = open('./data/1984.txt', 'r')
    for line in f.readlines():
        word = line.strip()
        if not (word in list1984) and not (word == ''):
            list1984.append(word)
    f.close()


def add_word(word, list1984):
    for i in list1984:
        if i == word:
            return False
    f = open('./data/1984.txt', 'a')
    f.write(word)
    f.write('\n')
    f.close()
    get(list1984)
    return True


def delete_word(word, list1984):
    dummy = []
    get(dummy)
    if word in dummy:
        f = open('./data/1984.txt', 'w')
        dummy.remove(word)
        for line in dummy:
            f.write(f"{line}\n")
        f.close()
        list1984[:] = dummy
        return True
    return False


