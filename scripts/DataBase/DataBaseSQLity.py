import sqlite3
from scripts.DataBase.AbstractDatabase import DatabaseInterface, Word, Sentence, Card,  Construction, Rule
from scripts.support.path import get_path_to_database


class SQLite(DatabaseInterface):
    con = sqlite3.connect(get_path_to_database())

    def get_all_words(self) -> list[Word]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT Spelling, Pronunciation, Translation FROM words')
            return [Word(spelling=spelling, pronunciation=pronunciation, translation=translation)
                    for spelling, pronunciation, translation in cur.fetchall()]

    def get_all_cards(self) -> list[Card]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT Name FROM Cards')
            return [Card(name=name) for name in cur.fetchall()]

    def get_all_sentences(self) -> list[Sentence]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT Translation,Sentence FROM Sentences')
            return [Sentence(translation=translation, sentence=sentence)
                    for translation, sentence in cur.fetchall()]

    def get_all_construction(self) -> list[Construction]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT Construction, Translation FROM Constructions')
            return [Construction(construction=construction, translation=translation)
                    for construction, translation in cur.fetchall()]

    def get_all_name_rules(self) -> list[Rule]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""SELECT Name FROM Rules""")
            return [Rule(name=name) for name in cur.fetchall()]

    def get_words_by_card(self, card) -> list[Word]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            SELECT Spelling, Pronunciation, Translation, Rang, TimeRepeat From Words as w
            Join Cards as c ON c.Name LIKE ?
            """, (card,))
            return [Word(spelling=spelling, pronunciation=pronunciation, translation=translation, rang=rang,
                         time_repeat=time_repeat)
                    for spelling, pronunciation, translation, rang, time_repeat in cur.fetchall()
                    ]

    def get_sentence_by_construction(self, construction) -> list[Sentence]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            Select Sentence, Sentences.Translation  FROM Sentences JOIN Constructions
            ON Constructions.Construction LIKE ?
            """, (construction,))
            return [Sentence(sentence=sentence, translation=translation)
                    for sentence, translation in cur.fetchall()]

    def get_rule(self, name) -> list[Rule]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            SELECT Name, Rule FROM Rules WHERE Name LIKE ?
            """, (name,))
            return [Rule(name=name, rule=rule)
                    for name, rule in cur.fetchall()]

    def get_id_by_name_card(self, name) -> list[Card]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""Select CardID From Cards where Name LIKE ?""", (name, ))
            return [Card(card_id=card_id) for card_id in cur.fetchall()]

    def get_id_by_construction(self, construction) -> list[Construction]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""Select constructionID From Constructions WHERE Construction LIKE ?""", (construction,))
            return [Construction(construction_id=cur.fetchall()[0][0])]

    def get_word_for_time_repeat(self) -> list[Word]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            Select WordID, Spelling, Pronunciation, Translation, Rang From Words Where TimeRepeat < DATETIME('now', 'localtime')
            """)
            return [Word(word_id=word_id, spelling=spelling, pronunciation=pronunciation, translation=translation, rang=rang)
                    for word_id, spelling, pronunciation, translation, rang in cur.fetchall()]

    def add_new_word(self, spelling, pronunciation, translate, cart_id, rang, time_repeat):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Words (Spelling, Pronunciation, Translation, CardID, Rang, TimeRepeat)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (spelling, pronunciation, translate, cart_id, rang, time_repeat, ))

    def add_new_card(self, name):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Cards (Name) VALUES (?)
            """, (name, ))

    def add_new_sentence(self, translation, construction_id, sentence):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Sentences (Translation, ConstructionID, Sentence)
            VALUES (?, ?, ?)
            """, (translation, construction_id, sentence))

    def add_new_construction(self, construction, translation):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Constructions (Construction, Translation)
            VALUES (?, ?)
            """, (construction, translation,))

    def set_time_for_word(self, word_id, time_repeat, rang):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            Update Words
            Set TimeRepeat = ?, Rang = ?
            where WordID = ?
            """, (time_repeat, rang, word_id, ))

    def save_rule(self, name, rule):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Rules (Name, Rule)
            VALUES (?, ?)
            """, (name, rule, ))
