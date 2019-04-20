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

    def result(self, answer):
        try:
            results = []

            for i in range(len(answer)):
                results.append(answer[i] == self.letters[i])

            for i in range(len(results)):
                if not results[i]:
                    self.words_without_letter[i] = self.words_without_letter[i].replace('_', self.letters[i])

            if all(results):
                text = 'Прекрасно, вы не сделали ни одной ошибки!'
            else:
                if any(results):
                    text = 'Что ж, вы сделали несколько ошибок. Продолжайте работать, и вас будет ждать успех.' + '\n\n'
                    text += 'Вот слова, в которых вы допустили ошибки:\n'

                else:
                    text = 'К сожалению, вы ошиблись везде, но не стоит отчаиваться\n'
                    text += 'Я уверна, что немного потрудившись, вы улучшите свои результаты\n.'
                    text += 'Постарайтесь запомнить как пишутся эти слова:\n'
                text += '\n'.join(self.words_without_letter[i] for i in range(len(self.words_without_letter)) if not results[i])
            return text
        except Exception:
            text = "Вы ввели неверное количество букв, я не могу соотнести ответы"
            return text

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
