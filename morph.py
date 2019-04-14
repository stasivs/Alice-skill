import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def key_translate(key):
    keys = {
        'NOUN': 'Существительное',
        'ADJF': 'Прилагательное(полное)',
        'ADJS': 'Прилагательное(краткое)',
        'COMP': 'Компраматив',
        'VERB': 'Глагол(личная форма)',
        'INFN': 'Глагол(инфинитив)',
        'PRTF': 'Причастие(полное)',
        'PRTS': 'Причастие(краткое)',
        'GRND': 'Деепричастие',
        'NUMR': 'Числительное',
        'ADVB': 'Наречие',
        'NPRO': 'Местоимение',
        'PRED': 'Предикатив',
        'PREP': 'Предлог',
        'CONJ': 'Союз',
        'PRCL': 'Частица',
        'INTJ': 'Междометие',
        'normal_form': 'Начальная форма',
        'POS': 'Часть речи',
        'animacy': 'Одушевлённость',
        'gender': 'Род',
        'number': 'Число',
        'perf': 'Совершенность',
        'case': 'Падеж',
        'nomn': 'именительный',
        'gent': 'родительный',
        'datv': 'дательный',
        'accs': 'винительный',
        'ablt': 'творительный',
        'loct': 'предложный',
        'voct': 'звательный',
        'gen1': 'первый родительный',
        'loc1': 'первый предложный',
        'gen2': 'второй родительный',
        'acc2': 'второй винительный',
        'loc2': 'второй предложный',
        'sing': 'единственное число',
        'plur': 'множественное число',
        'masc': 'мужской род',
        'femn': 'женский род',
        'neut': 'средний род',
        'LATN': 'латиница',
        'PNCT': 'пунктуация',
        'NUMB': 'число',
        'intg': 'целое число',
        'real': 'вещественное число',
        'ROMN': 'римское число',
        'UNKN': 'неизвестно',
        'aspect': 'Вид',
        'transitivity': 'Переходность',
        'tense': 'Время',
        'voice': 'Залог',
        'anim': 'Одушевленное',
        'inan': 'Неодушевленное',
        'GNdr': 'род не выражен',
        'ms-f': 'общий род (м/ж)',
        'Fixd': 'Неизменяемое',
        'Supr': 'Превосходная степень',
        'Qual': 'Качественное',
        'Apro': 'местоимение',
        'Anum': 'порядковое',
        'Poss': 'притяжательное',
        'impf': 'несовершенный вид',
        'tran': 'Переходный',
        'intr': 'Непереходный',
        'Impe': 'Безличный',
        'Mult': 'Многократный',
        'Refl': 'Возвратный',
        '1per': '1 лицо',
        '2per': '2 лицо',
        '3per': '3 лицо',
        'pres': 'настоящее время',
        'past': 'прошедшее время',
        'futr': 'будущее время',
        'indc': 'изъявительное наклонение',
        'impr': 'повелительное наклонение',
        'actv': 'действительный залог',
        'pssv': 'страдательный залог',
        'Infr': 'разговорное',
        'Slng': 'жаргонное',
        'Arch': 'устаревшее',
        'Litr': 'литературный вариант',
        'Erro': 'опечатка',
    }
    return keys[key]


def morphological_analysis(word):
    word_params = {}
    morph_word = morph.parse(word)[0]
    morph_tag = morph_word.tag
    # Начальная форма слова
    word_params["normal_form"] = morph_word.normal_form
    # Часть речи
    word_params["POS"] = morph_tag.POS
    # Одушевленность
    word_params["animacy"] = morph_tag.animacy
    # Вид
    word_params["aspect"] = morph_tag.aspect
    # Падеж
    word_params["case"] = morph_tag.case
    # Род
    word_params["gender"] = morph_tag.gender
    # Наклонение
    word_params["mood"] = morph_tag.mood
    # Число
    word_params["number"] = morph_tag.number
    # Лицо
    word_params["person"] = morph_tag.person
    # Время
    word_params["tense"] = morph_tag.tense
    # Переходность
    word_params["transitivity"] = morph_tag.transitivity
    # Залог
    word_params["voice"] = morph_tag.voice

    for key, value in list(word_params.items())[1:]:
        if value is None:
            del word_params[key]
        else:
            word_params[key] = key_translate(value).capitalize()
    word_params["normal_form"] = word_params["normal_form"].capitalize()
    return word_params


if __name__ == '__main__':
    print(morphological_analysis("Копье"))
    print(morphological_analysis("Быстро"))
    print(morphological_analysis("Бежать"))
    print(morphological_analysis("Красивый"))
    print(morphological_analysis("Бегающий"))
    print(morphological_analysis("Лежа"))
