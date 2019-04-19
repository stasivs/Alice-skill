from random import choice

from morph import morphological_analysis
from word_forms import return_word_forms


def get_suggests(user_id, sessionStorage):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests']
    ]

    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session

    return suggests


FIRST_ANSWER_SENTENSES = ['Привет! Давай займёмся русским языком!',
                          'Доброго времени суток! Хотите побазарить или поглаголить!',
                          'Гой еси, добрый молодец! Великий и могучий не ждёт!',
                          'Мир вашему дому! Желаете изучать русский?']

ENDING_DIALOG_ANSWERS = ['Что-нибудь ещё?',
                         'Может хотите ещё что-то разобрать?',
                         'Какие ещё услуги вас интересуют?',
                         'Бип-бип, жду приказаний, повелитель. Ха-ха']


def morphological_analise(req, res, curr_func, user_id):
    global sessionStorage
    for word in req['request']["original_utterance"].lower().split():
        if curr_func == 'Морфологический разбор слова':
            res['response']['text'] = '\n'.join(
                '{} : {}'.format(key, value) for key, value in morphological_analysis(
                    req['request']["original_utterance"].split()[
                        -1]).items()) + '\n\n' + choice(
                ENDING_DIALOG_ANSWERS)  # Функция для наморфологического разбора слова
            res['response']['end_session'] = True
            res['response']['buttons'] = get_suggests(user_id, sessionStorage)
            return ''
        if word in [
            'морфология слова',
            'морфологический разбор слова',
            'разбор слова',
            'разбор',
            'морфология'
        ]:
            res['response'][
                'text'] = 'Введите, пожалуйста, слово для разбора'  # Функция для наморфологического разбора слова
            res['response']['end_session'] = False
            return 'Морфологический разбор слова'
    else:
        return curr_func


def word_form(req, res, curr_func, user_id):
    for word in req['request']["original_utterance"].lower().split():
        if curr_func == 'Форма слова':
            res['response']['text'] = '\n'.join(
                i for i in
                return_word_forms(req['request']["original_utterance"].split()[-1])) + '\n\n' + choice(
                ENDING_DIALOG_ANSWERS)
            res['response']['end_session'] = True
            res['response']['buttons'] = get_suggests(user_id)
            return ''
        if word in [
            'форма слова',
            'форма',
            'форму'
        ]:
            res['response'][
                'text'] = 'Введите, пожалуйста, слово для анализа'  # Функция для формы слова
            res['response']['end_session'] = False
            return 'Форма слова'
    else:
        return curr_func


def farewell(req, res, curr_func):
    if req['request']["original_utterance"].lower() in [
        'спасибо нет',
        'спасибо не надо',
        'не надо',
        'нет',
        'отстань',
        'пока',
        'досвидания',
        'нет',
        'спасибо'
    ]:
        res['response']['text'] = 'Хорошего вам дня!'  # Завершение диалога
        res['response']['end_session'] = True
        return ''
    else:
        return curr_func
