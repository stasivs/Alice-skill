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
    #  -На морфологический разбор слова
    logging.info(req['request']["original_utterance"])
    logging.info(req['request']['command'])
    for word in req['request']["original_utterance"].lower().split():
        if curr_func == 'Морфологический разбор слова':
            res['response']['text'] = '\n'.join(
                '{} : {}'.format(key, value) for key, value in morphological_analysis(
                    req['request']["original_utterance"].split()[
                        -1]).items()) + '\n\n' + choice(ENDING_DIALOG_ANSWERS) # Функция для наморфологического разбора слова
            res['response']['end_session'] = True
            res['response']['buttons'] = get_suggests(user_id)
            curr_func = ''
            return
        if word in [
            'морфология слова',
            'морфологический разбор слова',
            'разбор слова',
            'разбор',
            'морфология'
        ]:
            curr_func = 'Морфологический разбор слова'

            res['response'][
                'text'] = 'Введите, пожалуйста, слово для разбора'  # Функция для наморфологического разбора слова
            res['response']['end_session'] = False
            logging.info(res)
            return

    #  -На диктант
    logging.info(req)
    for word in req['request']["original_utterance"].lower().split():
        if curr_func == 'Диктант':

            answer = req['request']['original_utterance'].lower().split()
            results = []
            right = dictation.words_without_letter.copy()

            for i in range(len(answer)):
                results.append(answer[i] == dictation.letters[i])

            for i in range(len(results)):
                if not results[i]:
                    right[i] = right[i].replace('_', dictation.letters[i])


            if all(results):
                res['response']['text'] = 'Прекрасно, вы не сделали ни одной ошибки!'
                res['response']['end_session'] = True
                res['response']['buttons'] = get_suggests(user_id)
                curr_func = ''
                return

            if any(results):
                res['response'][
                    'text'] = 'Что ж, вы сделали несколько ошибок. Продолжайте работать, и вас будет ждать успех.' + '\n\n'
                res['response']['text'] += 'Вот слова, в которых вы допустили ошибки:\n'
                res['response']['text'] += '\n'.join(right[i] for i in range(len(right)) if not results[i])
                res['response']['end_session'] = True
                res['response']['buttons'] = get_suggests(user_id)
                curr_func = ''
                return


            if not all(results):
                res['response']['text'] = 'К сожалению, вы ошиблись везде, но не стоит отчаиваться\n'
                res['response']['text'] += 'Я уверна, что немного потрудившись, вы улучшите свои результаты\n.'
                res['response']['text'] += 'Постарайтесь запомнить как пишутся эти слова:\n'
                res['response']['text'] += '\n'.join(right[i] for i in range(len(right)))
                res['response']['end_session'] = True
                res['response']['buttons'] = get_suggests(user_id)
                curr_func = ''
                return

        if word in [
            'диктант',
            'орфографический диктант',
            'орфография'
        ]:
            curr_func = 'Диктант'
            res['response'][
                'text'] = 'Правила такие:\n Я выводжу вам несколько слов с пропущенными буквами,\n а вы напишете правильные буквы через пробел:\n'  # Функция для диктанта
            dictation.clear()
            for i in range(randint(2, 6)):
                dictation.generate_word()
            res['response']['text'] += '\n'.join(i for i in dictation.words_without_letter)
            res['response']['end_session'] = False
            return

    #  -На форму слова
    for word in req['request']["original_utterance"].lower().split():
        if curr_func == 'Форма слова':
            res['response']['text'] = '\n'.join(
                i for i in
                return_word_forms(req['request']["original_utterance"].split()[-1])) + '\n\n' + choice(ENDING_DIALOG_ANSWERS)
            res['response']['end_session'] = True
            res['response']['buttons'] = get_suggests(user_id)
            curr_func = ''
            return
        if word in [
            'форма слова',
            'форма',
            'форму'
        ]:
            curr_func = 'Форма слова'
            res['response'][
                'text'] = 'Введите, пожалуйста, слово для анализа'  # Функция для формы слова
            res['response']['end_session'] = False
            logging.info(res)
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