from morph import *

morph = pymorphy2.MorphAnalyzer()


def return_word_forms(words):
    word_forms = [""] * 12

    cases = [
        {'nomn'},
        {'nomn', 'plur'},
        {'gent'},
        {'gent', 'plur'},
        {'datv'},
        {'datv', 'plur'},
        {'accs'},
        {'accs', 'plur'},
        {'ablt'},
        {'ablt', 'plur'},
        {'loct'},
        {'loct', 'plur'}
    ]

    for form in range(12):
        for tag in cases[form]:
            word_forms[form] += key_translate(tag) + " "
        word_forms[form] = word_forms[form].strip().capitalize() + ": "

    try:
        for word in words.split():
            word = morph.parse(word)[0]
            for form in range(12):
                word_forms[form] += word.inflect(cases[form])[0] + " "

        return [word_form.strip() for word_form in word_forms]
    except Exception:
        return ["Было введено несклоняемое слово"]


if __name__ == "__main__":
    print(return_word_forms("Тигран"))
    print(return_word_forms("Бегать"))
    print(return_word_forms("Ананас"))
