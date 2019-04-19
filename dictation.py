import random

with open("Dictionary.txt", "rt", encoding="utf8") as file:
    words = file.read().split()
    words[0] = words[0][1:]


class Dictation:
    def __init__(self):
        self.words_without_letter = []
        self.letters = []
        self.counter = 0

    def check(self, user_letter):
        self.counter += 1
        return user_letter == self.letters[self.counter]

    def generate_word(self):
        word = random.choice(words)
        num_of_letter = random.choice(range(1, len(word) - 1))
        while word[num_of_letter] in "- ":
            num_of_letter = random.choice(range(1, len(word) - 1))
        self.words_without_letter.append(word[:num_of_letter] + "_" + word[num_of_letter + 1:])
        self.letters.append(word[num_of_letter])

    def clear(self):
        self.words_without_letter = []
        self.letters = []
        self.counter = 0


if __name__ == "__main__":
    dict = Dictation()
    dict.generate_word()
    dict.generate_word()
    dict.generate_word()
    dict.generate_word()
    dict.generate_word()
    print(dict.words_without_letter)
    print(dict.letters)
