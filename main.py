# сделаю день который последний показывался(за него будет мало балов насчитываться) показывался + балы понимания
# и тогда эти балы будут влиять на то когда следующий раз будет показано слово.
# спршивать в боте через сколько дней повторить
# todo Переписать все на классы, а словарь вынести отдельно сделать json файлом или БД.
# + реализовать вариант перебора ВСЕ и сделать отдельные методы на повтор рус енг боз.
# todo сделать чтобы из программы можно было менять дату. Можно сделать сто дата просто умножается на два
#  и когда доходит до определеного числа повторяется уже раз в месяц.
#  Также можно сдела чтобы если мы нажали кнопку повтора то дата повтора этого слова скидывалась
#  на 1 день и начинала цикл с началаНо перед этим перегнать все в джейсон.
# + сделать отдельную проверку на lang
# todo сделать возможность повторять слова по сегодняшней дате.
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


import json
from colorama import Fore, Back, Style
from data import new_dict
import datetime

class Main:
    def __init__(self):
        self.list_data = ['Слова на сегодня']

    def all_data(self):
        """метод который собирает все даты слов и возвращает их пронумированым списком"""
        for key in new_dict.keys():
            if new_dict[key][0] not in self.list_data:
                self.list_data.append(new_dict[key][0])
        if 'Все слова' not in self.list_data:
            self.list_data.append('Все слова')
        return list(enumerate(self.list_data, 1))

    def need_to_repeat(self, key):
        """Метод который запрашивает у пользователя нужно ли ему повторить это слово если нужно
        то сохраняет его в блокнот для удобства."""
        print(Style.RESET_ALL)
        ans = input('Введите любой символ если хотите повторить слово.')
        if ans:
            with open('repeat.txt', 'a') as f:
                f.write(f'{new_dict[key][1]} - {key}\n')

    def foo(self):
        """метод который выводит слова с указаной датой и меняет ее на указаную. Есть пробелы
        для того чтобы увидеть слово
        data - определяет какое именно число нужно повторять слова"""
        time_now = datetime.datetime.now().strftime('%d.%m.%Y')
        date = self.check_data()
        lang = self.check_lang()
        for key in new_dict.keys():
            if date == 'Все слова':
                self.lenguage_identifier(lang, key)
            elif date == 'Слова на сегодня':
                if time_now in new_dict[key][0]:
                    self.lenguage_identifier(lang, key)
            elif date == new_dict[key][0]:  # Запрашиваем конкретную дату.
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
            self.painter(key, new_dict[key][1], key)
        elif lang == 'rus':
            self.painter(new_dict[key][1], key, key)
        elif lang == 'both':
            print(Fore.RED + f'{key} - {Fore.GREEN + new_dict[key][1]}')
            print(Style.RESET_ALL + f'\n{"*" * 80}')
            input()
        else:
            print(
                Style.RESET_ALL + 'Вы не ввели нужный язык, нужно сделать выбор между "rus", "eng", "both"')
            self.foo()

    def painter(self, first_value, second_value, key):
        """Метод для покраски слов"""
        print(Fore.RED + first_value)
        input(Style.RESET_ALL + 'Enter чтобы увидеть перевод')
        print(Fore.RED + first_value, '--> ', Fore.GREEN + second_value)
        self.need_to_repeat(key)
        print(Style.RESET_ALL + f'\n{"*" * 80}')



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
            json.dump(new_dict ,write_file, ensure_ascii=False, indent=4)


# b = FormatConverter(new_dict)

a = Main()
while True:
    a.foo()
