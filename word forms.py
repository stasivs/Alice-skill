import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def func(words):
    a = [""] * 12
    for word in words.split():
        word = morph.parse(word)[0]
        a[0] += word.inflect({'nomn'})[0] + " "
        a[1] += word.inflect({'nomn', 'plur'})[0] + " "
        a[2] += word.inflect({'gent'})[0] + " "
        a[3] += word.inflect({'gent', 'plur'})[0] + " "
        a[4] += word.inflect({'datv'})[0] + " "
        a[5] += word.inflect({'datv', 'plur'})[0] + " "
        a[6] += word.inflect({'accs'})[0] + " "
        a[7] += word.inflect({'accs', 'plur'})[0] + " "
        a[8] += word.inflect({'ablt'})[0] + " "
        a[9] += word.inflect({'ablt', 'plur'})[0] + " "
        a[10] += word.inflect({'loct'})[0] + " "
        a[11] += word.inflect({'loct', 'plur'})[0] + " "
    return [i.strip() for i in a]


print(func("Суп"))
print(func("Бегающий слава"))
print(func("Суп махровый"))
