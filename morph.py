import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def key_translate(tag):
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
        'nomn': 'именительный падеж',
        'gent': 'родительный падеж',
        'datv': 'дательный падеж',
        'accs': 'винительный падеж',
        'ablt': 'творительный падеж',
        'loct': 'предложный падеж',
        'voct': 'звательный падеж',
        'gen1': 'первый родительный падеж',
        'loc1': 'первый предложный падеж',
        'gen2': 'второй родительный падеж',
        'acc2': 'второй винительный падеж',
        'loc2': 'второй предложный падеж',
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
    return keys[tag]


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

    try:
        for key, value in list(word_params.items())[1:]:
            if value is not None:
                word_params[key_translate(key).capitalize()] = key_translate(value).capitalize()
            del word_params[key]

        word_params[key_translate("normal_form")] = word_params["normal_form"].capitalize()
        del word_params["normal_form"]
        return word_params
    except Exception:
        return {"Ошибка": "Невозможно выполнить морфологический разбор данного слова"}


if __name__ == "__main__":
    print(morphological_analysis("Копье"))
    print(morphological_analysis("Быстро"))
    print(morphological_analysis("Бежать"))
    print(morphological_analysis("Красивый"))
    print(morphological_analysis("Бегающий"))
    print(morphological_analysis("Лежа"))
