def get(list1984):
    f = open('1984.txt', 'r')
    for line in f.readlines():
        word = line.strip()
        if not (word in list1984) and not (word == ''):
            list1984.append(word)
    f.close()


def add_word(word, list1984):
    f = open('1984.txt', 'a')
    f.write(word)
    f.write('\n')
    f.close()
    get(list1984)


def delete_word(list1984, word):
    dummy = []
    get(dummy)
    f = open('1984.txt', 'w')
    if word in dummy:
        dummy.remove(word)
    for line in dummy:
        f.write(f"{line}\n")
    f.close()
    list1984[:] = dummy


