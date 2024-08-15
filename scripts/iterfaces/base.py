import random
import webbrowser
from datetime import datetime
from unittest import case

from scripts.DataBase.DataBaseSQLity import SQLite
from scripts.DataBase.AbstractDatabase import DatabaseInterface, Card, Word, Sentence, Construction, Rule
from scripts.support.format import paint
from datetime import timedelta
from scripts.support.path import get_path_to_file_temp

import os

forget_table = [
        (-1, 480, 900, 345600),
        (-1, 259200, 518400, 691200),
        (-1, 345600, 777600, 950400)
         ]


class Do:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def add_new_words(self):
        print()
        while True:
            print(
                f'Chose a card name to add a new word or command:\n'
                f'{paint('help()', 'green')} -- print all name card.\n'
                f'{paint("exit()", 'red')} -- return to main menu.\n'
            )
            command = input(f'{paint('Enter: ', 'orange')}')
            match command:
                case 'help()':
                    print()
                    print(f'=========================')
                    for numer, card in enumerate(self.db.get_all_cards(), 1):
                        print(f'{numer}. {paint(*card.name, 'green')}')
                    print(f'=========================')
                    print()
                case 'exit()':
                    break
                case _ as name_card:
                    record: list[Card] = self.db.get_id_by_name_card(name_card)

                    if not record:
                        print()
                        print(f'{paint('It\'s card doesn\'t exist!', 'red')}\n')
                        continue

                    card: Card = record[0]
                    print(f'{paint('exit()', 'red')} -- finish adding new words.')
                    while True:
                        print(f'=========================')

                        spelling = input(f'Enter a {paint('spelling',  'green')}: ')

                        if spelling == 'exit()':
                            break

                        pronunciation = input(f'Enter a {paint('pronunciation',  'green')}: ')
                        translation = input(f'Enter a {paint('translation',  'green')}: ')
                        rang = 0
                        time_repeat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        data = [
                            spelling,
                            pronunciation,
                            translation,
                            card.card_id[0],
                            rang,
                            time_repeat
                        ]
                        self.db.add_new_word(*data)
                        print(f'=========================')
                        print()

    def add_new_card(self):
        print(f'=========================')
        name = input(f'{paint("Enter a card name to add", 'orange')}: ')
        self.db.add_new_card(name)
        print(f'=========================')

    def add_new_construction(self):
        print()
        print(f'=========================')
        construction = input(f'{paint("Enter a construction", 'orange')}: ')
        translation = input(f'{paint("Enter a translation", 'orange')}: ')
        self.db.add_new_construction(construction, translation)
        print(f'=========================')

    def add_new_sentence(self):

        while True:
            print(f'1. {paint('help()', 'green')} -- print all construction.\n'
                  f'2. {paint('exit()', 'red')} -- return to main menu.\n')
            construction = input(f'{paint("Enter a construction or a command", 'orange')}: ')

            match construction:
                case 'help()':
                    print()
                    print(f'=========================')
                    for number, record in enumerate(self.db.get_all_construction(), 1):
                        print(f'{number}. {paint(f'{record.construction}', 'orange')} -- {record.translation}')
                    print(f'=========================')
                case 'exit()':
                    break
                case _ as construction:
                    the_construction: Construction = self.db.get_id_by_construction(construction)[0]

                    while not the_construction.construction_id:
                        print(f'{paint('Invalid construction', 'red')}\n')
                        construction = input(f'{paint("Enter a construction", 'orange')}: ')
                        the_construction: Construction = self.db.get_id_by_construction(construction)[0]
                    print()
                    print(f'=========================')
                    sentence = input(f'{paint("Enter a sentence", 'orange')}: ')
                    translation = input(f'{paint("Enter a translation", 'orange')}: ')
                    print(f'=========================')
                    print()

                    self.db.add_new_sentence(sentence, the_construction.construction_id, translation)

    def repeat_word(self):
        print(f'=========================')
        while True:
            command = input(f'Chose a command or enter name of card:\n'
                            f'{paint('all()', 'green')} -- mod survival.\n'
                            f'{paint('card()', 'orange')} -- repeat words by cards.\n'
                            f'{paint('time()', 'orange')} -- mod time.\n'
                            f'{paint("exit()", 'red')} -- return to main menu.\n')
            match command:
                case 'all()':
                    records = self.db.get_all_words()
                    for record in records:
                        language = random.randint(0, 1)
                        if language:
                            term = record.translation
                        else:
                            term = record.spelling
                        print()
                        print(f'=========================')
                        print(f'Word: {paint(term, 'green')}')
                        input('...')
                        print(f'Pronunciation: |{record.pronunciation[0]}|')

                        if language:
                            term = record.spelling[0]
                        else:
                            term = record.translation[0]
                        print(f'Translation: {term}')
                        print(f'=========================')

                case 'time()':
                    records = self.db.get_word_for_time_repeat()
                    for record in records:
                        print(f'=========================')
                        language = random.randint(0, 1)

                        if language:
                            term = record.translation
                        else:
                            term = record.spelling

                        print(f'Word: {paint(term, 'purple')}')
                        print(f'1. {paint('again', 'red')}, 2. {paint('hard', 'orange')}, '
                              f'3. {paint('good', 'green')}, 4. {paint('easy', 'cyan')}')

                        the_rang = input('Enter rang: ')
                        while the_rang not in ['1', '2', '3', '4']:
                            the_rang = input('Enter rang: ')
                        the_rang = int(the_rang) - 1

                        delta = (datetime.now() + timedelta(seconds=forget_table[int(record.rang)][the_rang])).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        input('...')

                        rang = int(record.rang)
                        if the_rang != 0:
                            rang = rang + 1 if rang < 2 else 2
                        else:
                            rang = rang - 1 if rang != 0 else 0

                        if language:
                            term = record.spelling
                        else:
                            term = record.translation

                        self.db.set_time_for_word(record.word_id, delta, rang)

                        print(f'Translation: {term}\n'
                              f'Pronunciation: {record.pronunciation}')
                        print(f'=========================')
                        input(f'...')

                case 'card()':
                    while True:
                        print(
                            f'Chose a command or enter name of card:\n'
                            f'{paint('help()', 'green')} -- print all card .\n'
                            f'{paint('exit()', 'red')} -- finish repeat words.\n'
                        )
                        command = input(f'{paint('Enter', 'orange')}: ')

                        if command == 'help()':
                            print()
                            records = self.db.get_all_cards()
                            print(f'=========================')

                            for number, record in enumerate(records, 1):
                                print(f'{number}. {paint(record.name[0], 'orange')}')
                            print(f'=========================')
                            print()
                        elif command == 'exit()':
                            break
                        else:
                            records = self.db.get_words_by_card(command)
                            for record in records:
                                language = random.randint(0, 1)
                                if language:
                                    term = record.translation
                                else:
                                    term = record.spelling
                                print()
                                print(f'=========================')
                                print(f'Word: {paint(term, 'green')}')

                                if input('...') == 'exit()':
                                    break

                                print(f'Pronunciation: |{record.pronunciation}|')

                                if language:
                                    term = record.spelling
                                else:
                                    term = record.translation
                                print(f'Translation: {term}')
                                print(f'=========================')

                case 'exit()':
                    print(f'=========================')
                    break
                case _:
                    print(f'{paint('Invalid command!', 'red')}')

    def repeat_sentence(self):
        print('Chose')
        print(f'{paint('all()', 'green')} -- chose all sentences.\n'
              f'{paint('construction()', 'green')} -- repeat sentence by construction.\n'
              f'{paint('exit()', 'red')} -- return to main manu.')
        print()
        while True:
            command = input(f'{paint('Enter: ', 'orange')}')
            match command:
                case 'all()':
                    records = self.db.get_all_sentences()
                    for record in records:
                        print(f'=========================')
                        print(f'{paint('Sentence', 'green')}:\n{record.translation}')
                        input('...')
                        print(f'{paint('Translation', 'green')}\n{record.sentence}')
                        print('...')
                        print(f'=========================')
                        print()

                case 'construction()':
                    while True:
                        print(f'Enter construction or command: ')
                        print(f'1. {paint('help()', 'green')} -- print all construction.\n'
                              f'2. {paint('exit()', 'red')} -- finish repeat construction.')
                        command = input('Enter: ')
                        if command == 'help()':
                            records = self.db.get_all_construction()
                            print(f'=========================')
                            for number, construction in enumerate(records, 1):
                                print(f'{number}. {paint(f'{construction.construction}/{construction.translation}',  'orange')}')
                            print(f'=========================')
                        elif command == 'exit()':
                            break

                        else:
                            records = self.db.get_sentence_by_construction(command)
                            if not records:
                                print(f'{print('Incorrect command!', 'red')}')
                                command = input('Enter: ')
                                records = self.db.get_sentence_by_construction(command)

                                for record in records:
                                    print(f'=========================')
                                    print(f'{paint('Sentence:', 'green')}\n')
                                    print(record.translation[0])
                                    input('...')
                                    print(f'{paint('Translation:', 'green')}\n')
                                    print(record.sentence[0])
                                    print(f'=========================')
                                    print()
                                    print('...')

                case 'exit()':
                    break

    def repeat_rule(self):
        while True:
            print('Chose a rule or a command:\n')
            print(f'{paint('help()', 'green')} -- print all rules.\n'
                  f'{paint('exit()', 'red')} -- return to main manu.')
            command = input(f'{paint('Enter: ', 'orange')}')
            match command:
                case 'help()':
                    print(f'=========================')
                    for number, record in enumerate(self.db.get_all_name_rules(), 1):
                        print(f'{number}. {paint(record.name[0], 'green')}')
                    print(f'=========================')
                case 'exit()':
                    break
                case _ as rule:
                    record = self.db.get_rule(rule)
                    if not record:
                        print(f'{print('Incorrect rule!', 'red')}')
                        continue
                    else:
                        rule = record[0]

                        with open(get_path_to_file_temp('rule.html'), 'w') as file:
                            print(rule.rule)
                            file.write(rule.rule)
                        webbrowser.open(get_path_to_file_temp('rule.html'))


class Interface:
    do = Do(SQLite())

    @staticmethod
    def run():
        while True:
            print(
                f'Enter a number of command:\n\n'
                f'1. Add new words.\n'
                f'2. Add a new card.\n'
                f'3. Add a new construction.\n'
                f'4. Add a new sentence.\n'
                f'5. Repeat the words.\n'
                f'6. Repeat the sentences.\n'
                f'7. Repeat the rules.\n'
                f'8. {paint('exit()', 'red')}\n'
            )
            command = input(f'{paint('Enter your command: ', 'orange')}')

            match command:
                case '1':
                    Interface.do.add_new_words()
                case '2':
                    Interface.do.add_new_card()
                case '3':
                    Interface.do.add_new_construction()
                case '4':
                    Interface.do.add_new_sentence()
                case '5':
                    Interface.do.repeat_word()
                case '6':
                    Interface.do.repeat_sentence()
                case '7':
                    Interface.do.repeat_rule()
                case 'exit()':
                    exit()
                case _:
                    print(f'{paint('Invalid command!', 'red')}\n')


if __name__ == '__main__':
    Interface.run()
