# импортируем библиотеки
from flask import Flask, request
import logging
from random import choice
import json

app = Flask(__name__)

logging.basicConfig(level=logging.ERROR)

sessionStorage = {}

FIRST_ANSWER_SENTENSES = ['Привет! Давай займёмся русским языком!',
                          'Доброго времени суток! Хотите побазарить или поглаголить!',
                          'Гой еси, добрый молодец! Великий и могучий не ждёт!',
                          'Мир вашему дому! Желаете изучать русский?']


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
    user_id = req['session']['user_id']
    mode = ''

    answered_word = get_answered_word(req)
    if len(answered_word) == 1:
        pass

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Морфологический разбор слова",
                "Орфографический диктант",
                "Форма слова"
            ]
        }
        res['response']['text'] = choice(FIRST_ANSWER_SENTENSES)
        res['response']['buttons'] = get_suggests(user_id)
        return

    #  Обработка ответов:
    #  -На морфологический разбор слова
    if req['request']["original_utterance"].lower() in [
        'морфология слова',
        'морфологический разбор слова',
        'разбор слова',
        'разбор'
    ]:
        res['response']['text'] = '\n'.join(
            '{} : {}'.format() for i in [])  # Функция для наморфологического разбора слова
        res['response']['end_session'] = True
        mode = ''
        return

    #  -На диктант
    if req['request']["original_utterance"].lower() in [
        'диктант',
        'орфографический диктант',
        'орфография'
    ]:
        res['response']['text'] = '<>'  # Функция для диктанта
        res['response']['end_session'] = False
        return

    #  -На форму слова
    if req['request']["original_utterance"].lower() in [
        'форма слова',
        'форма',
        'форму'
    ]:
        res['response']['text'] = '<>'  # Функция для формы слова
        res['response']['end_session'] = False
        return

    #  -Прощание
    if req['request']["original_utterance"].lower() in [
        'спасибо нет',
        'спасибо не надо',
        'не надо',
        'нет',
        'отстань',
        'пока',
        'досвидания',
    ]:
        res['response']['text'] = 'Хорошего вам дня!'  # Завершение диалога
        res['response']['end_session'] = True
        return


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests']
    ]

    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
