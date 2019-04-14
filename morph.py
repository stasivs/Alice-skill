import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def key_translate(key):
    keys = {'NOUN': 'Существительное',
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
            'nomn': 'иминительный',
            'gent': 'родительный',
            'datv': 'дательный',
            'accs': 'винительный',
            'ablt': 'творительный',
            'loct': 'предложный',
            'voct': 'звательный',
            'gen2': 'второй родительный',
            'acc2': 'второй винительный',
            'loc2': 'второй предложный',
            'sign': 'единственное число',
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
    # Наклонение3
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

    trans = {}

    for key, value in list(word_params.items()):
        if value is None:
            del word_params[key]
        else:

            trans[key_translate(key)] = morph.lat2cyr(word_params[key])

    return trans


if __name__ == '__main__':
    morphological_analysis("Копье")
    morphological_analysis("Быстро")
    morphological_analysis("Бежать")
    morphological_analysis("Красивый")
    morphological_analysis("Бегающий")
    morphological_analysis("Лежа")
