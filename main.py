# сделаю день который последний показывался(за него будет мало балов насчитываться) показывался + балы понимания
# и тогда эти балы будут влиять на то когда следующий раз будет показано слово.
# спршивать в боте через сколько дней повторить
# todo Переписать все на классы, а словарь вынести отдельно сделать json файлом.
# + did реализовать вариант перебора ВСЕ и сделать отдельные методы на повтор рус енг боз.
# todo сделать чтобы из программы можно было менять дату. Но перед этим перегнать все в джейсон.
# todo сделать отдельную проверку на lang

import json
from colorama import Fore, Back, Style
from data import new_dict


# def json_creator(new_dict):
#     '''Фунция преобразования dict в json'''
#     with open("data_file.json", "w", encoding='utf-8') as write_file:
#         json.dump(new_dict ,write_file, ensure_ascii=False, indent=4)

class Main:
    def __init__(self):
        self.list_data = []

    def all_data(self):
        """метод который собирает все даты слов и возвращает их пронумированым списком"""
        for key in new_dict.keys():
            if new_dict[key][0] not in self.list_data:
                self.list_data.append(new_dict[key][0])
        if 'Все' not in self.list_data:
            self.list_data.append('Все')
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
        date = self.data()
        lang = input('Напишите rus или eng или both. Чтобы выбрать язык:\n')
        for key in new_dict.keys():
            if date == 'Все':
                self.lenguage_identifier(lang, key)
            elif new_dict[key][0] == date:  # Запрашиваем конкретную дату.
                self.lenguage_identifier(lang, key)

    def data(self):
        """Метод определяющий дату повтора"""
        while True:
            data_value = int(input(
                f'Введите цифру которая присвоенна дате которую хотите повторить {self.all_data()}\n'))
            if data_value > len(self.all_data()):
                print('Вы ввели неправильный номер.')
            else:
                return self.all_data()[data_value - 1][1]

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
            print(Style.RESET_ALL + 'Вы не ввели нужный язык, нужно сделать выбор между "rus", "eng", "both"')
            self.foo()

    def painter(self, first_value, second_value, key):
        """Метод для покраски слов"""
        print(Fore.RED + first_value)
        input(Style.RESET_ALL + 'Enter чтобы увидеть перевод')
        print(Fore.RED + first_value, '--> ', Fore.GREEN + second_value)
        self.need_to_repeat(key)
        print(Style.RESET_ALL + f'\n{"*" * 80}')


a = Main()
while True:
    a.foo()

