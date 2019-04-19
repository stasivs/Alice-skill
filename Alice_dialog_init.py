# импортируем библиотеки
import json
import logging
from random import choice, randint

from flask import Flask, request
from dictation import Dictation
from morph import morphological_analysis
from word_forms import return_word_forms

dictation = Dictation()

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
curr_func = ''
sessionStorage = {}

FIRST_ANSWER_SENTENSES = ['Привет! Давай займёмся русским языком!',
                          'Доброго времени суток! Хотите побазарить или поглаголить!',
                          'Гой еси, добрый молодец! Великий и могучий не ждёт!',
                          'Мир вашему дому! Желаете изучать русский?']

ENDING_DIALOG_ANSWERS = ['Что-нибудь ещё?',
                         'Может хотите ещё что-то разобрать?',
                         'Какие ещё услуги вас интересуют?',
                         'Бип-бип, жду приказаний, повелитель. Ха-ха']


def get_entities(json):
    entities = json['request']['entities']
    return entities


def get_answered_word(req):
    word = list()
    word.append(req['request']['command'])
    return word


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    return json.dumps(response)


def handle_dialog(req, res):
    global curr_func
    functions = ["Морфологический разбор", "Диктант", "Форма слова"]

    # Слова для морфологического разбора
    init_morph_words = [
        'морфология слова',
        'морфологический разбор слова',
        'разбор слова',
        'разбор',
        'морфология'
    ]

    # Слова для начала диктанта
    init_dictantion_words = [
        'диктант',
        'орфографический диктант',
        'орфография'
    ]

    # Слова для начала спряжения
    init_forms_words = [
        'форма слова',
        'форма',
        'форму'
    ]

    # Слова для конца диалога
    end_words = [
        'спасибо нет',
        'спасибо не надо',
        'не надо',
        'нет',
        'отстань',
        'пока',
        'досвидания',
    ]

    user_id = req['session']['user_id']
    answered_word = get_answered_word(req)
    if len(answered_word) == 1:
        pass

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Морфологический разбор слова",
                "Орфографический диктант",
                "Форма слова",
            ]
        }
        res['response']['text'] = choice(FIRST_ANSWER_SENTENSES)
        res['response']['buttons'] = get_suggests(user_id)
        return

    #  Обработка ответов:
    #  - На морфологический разбор слова
    logging.info(req['request']["original_utterance"])
    logging.info(req['request']['command'])

    text = req['request']['original_utterance'].lower()

    if text in init_morph_words:
        curr_func = functions[0]
        res['response']['text'] = 'Введите, пожалуйста, слово для разбора'  # Функция для формы слова
        res['response']['end_session'] = False
        logging.info(res)
        return

    # Обработка ответов:
    # - На диктант
    if text in init_dictantion_words:
        curr_func = functions[1]
        res['response']['text'] = 'Правила такие:\n Я выводжу вам несколько слов с пропущенными буквами,\n ' \
                                  'а вы напишете правильные буквы через пробел:\n'  # Функция для диктанта  # Функция для формы слова
        dictation.clear()
        for i in range(randint(2, 6)):
            dictation.generate_word()
        res['response']['text'] += '\n'.join([str(i) for i in dictation.words_without_letter])
        res['response']['end_session'] = False
        logging.info(res)
        return

    # Обработка ответов:
    # - На формы слова
    if text in init_forms_words:
        curr_func = functions[2]
        res['response']['text'] = 'Введите, пожалуйста, слово для анализа'  # Функция для формы слова
        res['response']['end_session'] = False
        logging.info(res)
        return

    #  -Прощание
    if text in end_words:
        res['response']['text'] = 'Хорошего вам дня!'  # Завершение диалога
        res['response']['end_session'] = True
        return

    if curr_func == functions[0]:
        res['response']['text'] = '\n'.join(
            '{} : {}'.format(key, value) for key, value in morphological_analysis(
                req['request']["original_utterance"].split()[
                    -1]).items()) + '\n\n' + choice(
            ENDING_DIALOG_ANSWERS)  # Функция для наморфологического разбора слова
        res['response']['end_session'] = True
        res['response']['buttons'] = get_suggests(user_id)
        curr_func = ''
        return

    if curr_func == functions[1]:
        answer = req['request']['original_utterance'].lower().split()
        res['response']['text'] = dictation.result(answer)
        res['response']['end_session'] = True
        res['response']['buttons'] = get_suggests(user_id)
        curr_func = ''
        return

    if curr_func == functions[2]:
        res['response']['text'] = '\n'.join(
            i for i in
            return_word_forms(req['request']["original_utterance"].split()[-1])) + '\n\n' + choice(
            ENDING_DIALOG_ANSWERS)
        res['response']['end_session'] = True
        res['response']['buttons'] = get_suggests(user_id)
        curr_func = ''
        return

    res['response']['text'] = 'Простите, я вас не поняла, повторите, пожалуйста.'
    res['response']['end_session'] = False
    return


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests']
    ]

    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session

    return suggests


if __name__ == '__main__':
    app.run(debug=True)