import random


def five_letter_words():
    """ Return text file containing only five letter words from list of words.
        Function only included to show working.
    """
    f = open("engmix.txt", "r")

    five = []
    for x in f:
        if len(x) == 6:
            five.append(x)
    f.close()

    with open('five.txt', 'w') as f:
        for x in five:
            f.write(x)
    f.close()


def file_to_word_set(filepath):
    """ Return list from text file.
        Each element is the line of the file (here, a five letter word).
    """
    f = open(filepath, "r")
    words = f.read()
    word_list = words.split("\n")
    f.close()
    return set(word_list[:-1])


def find_best_word(words):
    letter_popularity = letter_count(words)
    for allow_repeats in [False, True]:
        i = 3
        while i <= len(letter_popularity):
            best_letters = letter_popularity[:i]
            good_words = word_search(words, best_letters, allow_repeats)
            if good_words:
                return good_words
            i += 1


def letter_count(words):
    """ Return list of letters in order of the number of occurences each letter
        has in the word list (from most to least).
    """
    letter_count = {}
    for word in words:
        for letter in word:
            letter_count[letter] = letter_count.setdefault(letter, 0) + 1
    letter_popularity = sorted(letter_count, key=letter_count.get, reverse=True)
    return letter_popularity


def word_search(words, best_letters, allow_repeats):
    good_words = []
    for word in words:
        if recursive_letter_search(word, best_letters, 0, allow_repeats):
            good_words.append(word)
    return good_words


def recursive_letter_search(word, best_letters, index, allow_repeats):
    if index == 5:
        return word
    current_letter = word[index]
    for best_letter in best_letters:
        if best_letter == current_letter:
            if not allow_repeats:
                best_letters.remove(best_letter)
            value = recursive_letter_search(word, best_letters, index+1, allow_repeats)
            if not allow_repeats:
                best_letters.append(best_letter)
            if value:
                return value
    return False


def word_cycle(words):
    while True:
        good_words = find_best_word(words)
        good_word = random.choice(good_words)
        words.remove(good_word)
        print("Enter: " + good_word)
        new_word = input("Type 'end' if this is the correct word, if you want to enter a different word type the word, otherwise press enter: \n") or good_word
        if new_word == 'end':
            break
        orange = set(input("Which letters are orange? (format: \"a,w,s\"): \n").split(','))
        green = set(input("Which letters are green? (format: \"a,w,s\"): \n").split(','))
        words = remove_words(words, new_word, orange, green)


def remove_words(words, good_word, orange, green):
    not_in_word = set()
    # {letter:index}, e.g. arose with green a,s gives: {'a':0,'s':3}
    green_dict = {}
    orange_dict = {}
    for i, letter in enumerate(good_word):
        if letter in green:
            green_dict[letter] = i
        elif letter in orange:
            orange_dict[letter] = i
        else:
            not_in_word.add(letter)
    new_words = set()
    for word in words:
        if is_word_possible(word, orange_dict, green_dict, not_in_word):
            new_words.add(word)
    print("Possible words: ")
    print(new_words)
    print("\n")
    return new_words


def is_word_possible(word, orange_dict, green_dict, not_in_word):
    for green_letter, index in green_dict.items():
        if word[index] != green_letter:
            return False
    for orange_letter, index in orange_dict.items():
        if orange_letter not in word:
            return False
        if word[index] == orange_letter:
            return False
    for letter in word:
        if letter in not_in_word:
            return False
    return True


if __name__ == "__main__":
    words = file_to_word_set("five.txt")
    word_cycle(words)
