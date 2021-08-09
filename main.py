# сделаю день который последний показывался(за него будет мало балов насчитываться) показывался + балы понимания
# и тогда эти балы будут влиять на то когда следующий раз будет показано слово.
# спршивать в боте через сколько дней повторить
# todo Переписать все на классы, а словарь вынести отдельно сделать json файлом или БД.
# + реализовать вариант перебора ВСЕ и сделать отдельные методы на повтор рус енг боз.
# todo сделать чтобы из программы можно было менять дату. Можно сделать что дата просто умножается на два
#  и когда доходит до определеного числа повторяется уже раз в месяц.
#  Также можно сделать чтобы если мы нажали кнопку повтора то дата повтора этого слова скидывалась
#  на 1 день и начинала цикл с начально перед этим перегнать все в джейсон.
# + сделать отдельную проверку на lang
# + сделать возможность повторять слова по сегодняшней дате.
# todo сделать озвучку русских и английских слов
# + Версионость
# todo сделать README документ
# todo Сделать отдельный класс который будет преобразовать из словаря в джейсон иди в бд и так далее.

# Version 1.01 Добавил возможность повторить все слова за сегодня.
# Version 1.02
# 1) Изменен вывод возможных повторов дат с горизонтального на вертикальный удалено.
# 2) Сделаны исравления для лучшего понимая с "Сегодня" на "Слова на сегодня"  и с "Все" на "Все Слова"
# 3) Найдена и исправлена ошибка когда вводили буквеный ввод при выборе повтора даты.
# 4) Сделал отдельную проверку на язык повтора.
# Version 1.03
# Добавил метод words_counter() - который подсчитывает количество слов в словаре.

from gtts import gTTS
from colorama import Fore, Back, Style

import json
import datetime

from data import vocabulary_dict
from on_study import study_dict


class Main:
    time_now = datetime.datetime.now().strftime('%d.%m.%Y')
    def __init__(self):
        self.list_data = ['Слова на сегодня']

    def all_data(self):
        """метод который собирает все даты слов и возвращает их пронумированым списком"""
        for key in vocabulary_dict.keys():
            if vocabulary_dict[key][0] not in self.list_data:
                self.list_data.append(vocabulary_dict[key][0])
        if 'Все слова' not in self.list_data:
            self.list_data.append('Все слова')
        return list(enumerate(self.list_data, 1))

    def need_to_repeat(self, key):
        """Метод который запрашивает у пользователя нужно ли ему повторить это слово если нужно
        то сохраняет его в блокнот для удобства."""
        print(Style.RESET_ALL)
        input_1 = input('Введите любой символ если хотите повторить слово.')
        if input_1:
            with open('repeat.txt', 'a') as f:
                f.write(f'{vocabulary_dict[key][1]} - {key}\n')

    def chooser_date(self):
        """метод который выводит слова с указаной датой и запрашивает у пользователя за какой периуд
        он хочет их повторить. Есть пробелы для того чтобы увидеть слово.
        data - определяет какое именно число нужно повторять слова"""
        date = self.check_data()
        lang = self.check_lang()
        for key in vocabulary_dict.keys():
            if date == 'Все слова':
                self.lenguage_identifier(lang, key)
            elif date == 'Слова на сегодня':
                if self.time_now in vocabulary_dict[key][0]:
                    self.lenguage_identifier(lang, key)
            elif date == vocabulary_dict[key][0]:  # Запрашиваем конкретную дату.
                self.lenguage_identifier(lang, key)

    def check_lang(self):
        """Метод проверки правильности ввода языка"""
        while True:
            lang = input('Напишите rus или eng или both. Чтобы выбрать язык:\n')
            if lang in ['rus', 'eng', 'both']:
                return lang

    def check_data(self):
        """Метод определяющий дату повтора"""
        all_dates_to_repeat = self.all_data()
        while True:
            print(f'Введите цифру которая присвоенна дате которую хотите повторить')
            for date_tuple in all_dates_to_repeat:
                print(date_tuple)
            data_value = input()
            if not data_value.isdigit():
                print('Нужно ввести номер даты которую вы хотите повторить.')
            elif int(data_value) > len(self.all_data()):
                print('Вы ввели неправильный номер.')
            else:
                return self.all_data()[int(data_value) - 1][1]

    def lenguage_identifier(self, lang, key):
        """Метод определяющий язык"""
        if lang == 'eng':
            self.painter(key, vocabulary_dict[key][1], key)
        elif lang == 'rus':
            self.painter(vocabulary_dict[key][1], key, key)
        elif lang == 'both':
            print(Fore.RED + f'{key} - {Fore.GREEN + vocabulary_dict[key][1]}')
            print(Style.RESET_ALL + f'\n{"*" * 80}')
            input()
        else:
            print(
                Style.RESET_ALL + 'Вы не ввели нужный язык, нужно сделать выбор между "rus", "eng", "both"')
            self.chooser_date()

    def painter(self, first_value, second_value, key):
        """Метод для покраски слов"""
        print(Fore.RED + first_value)
        input(Style.RESET_ALL + 'Enter чтобы увидеть перевод')
        print(Fore.RED + first_value, '--> ', Fore.GREEN + second_value)
        self.need_to_repeat(key)
        print(Style.RESET_ALL + f'\n{"*" * 80}')
        
    def speacker(self):
        # all_dict = {**study_dict, **vocabulary_dict} # все слова
        all_dict = {**study_dict} # слова на изучении
        # all_dict = {**vocabulary_dict} # изученые слова
        for eng_string, ru_string in all_dict.items():
            print(f'{eng_string}-{ru_string[1]}') # показывает слова котрые записывает в аудио файл.
            tts_en = gTTS(eng_string, lang='en')
            tts_ru = gTTS(ru_string[1], lang='ru')

            with open('test.mp3', 'ab') as f:
                tts_en.write_to_fp(f)

            with open('test.mp3', 'ab') as f:
                tts_ru.write_to_fp(f)


    def words_counter(self):
        """Метод который показует количество слов в словаре"""
        return len(vocabulary_dict)

class FormatConverter:
    def __init__(self, array):
        self.array = self.check_array(array)

    def check_array(self, array):
        """Функция определяет к какому типу данных принадлежит передаваемый массив."""
        if isinstance(array, dict):
            self.json_creator(array)
     
    def json_creator(self, array):
        '''Фунция преобразования dict в json'''
        with open("data_file.json", "w", encoding='utf-8') as write_file:
            json.dump(vocabulary_dict ,write_file, ensure_ascii=False, indent=4)
    

b = FormatConverter(1)

a = Main()
# print(a.words_counter())
# while True:
#     a.chooser_date()
a.speacker()