import pymorphy2

morph = pymorphy2.MorphAnalyzer()


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

    trans = {}

    for key, value in list(word_params.items()):
        if value is None:
            del word_params[key]
        else:
            trans[key] = morph.lat2cyr(word_params[key])
    print(word_params)
    print(trans)
    print()


morphological_analysis("Копье")
morphological_analysis("Быстро")
morphological_analysis("Бежать")
morphological_analysis("Красивый")
morphological_analysis("Бегающий")
morphological_analysis("Лежа")
