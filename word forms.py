import pymorphy2

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
    
    for word in words.split():
        word = morph.parse(word)[0]
        for form in range(12):
            word_forms[form] += word.inflect(cases[form])[0] + " "        
    
    return [word_form.strip() for word_form in word_forms]


print(return_word_forms("Суп"))
print(return_word_forms("Бегающий слава"))
print(return_word_forms("Суп махровый"))
