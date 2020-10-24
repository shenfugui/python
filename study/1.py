def in_both(word1, word2):
    for i in word1:
        if i in word2:
            print(i)


def main():
    word1 = "hello"
    word2 = "world"
    in_both(word1, word2)


if __name__ == '__main__':
    main()
