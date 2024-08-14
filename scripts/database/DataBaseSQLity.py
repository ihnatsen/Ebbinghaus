import sqlite3
import interface_data_base


class SQLite(interface_data_base.Skeleton):
    con = sqlite3.connect('database.db')

    def get_all_words(self) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM words')
            return cur.fetchall()

    def get_all_cards(self) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Cards')
            return cur.fetchall()

    def get_all_sentences(self) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Sentences')
            return cur.fetchall()

    def get_all_construction(self) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Constructions')
            return cur.fetchall()

    def get_all_name_rules(self) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""SELECT Name FROM Rules""")
            return cur.fetchall()

    def get_words_by_card(self, card) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            SELECT Spelling, Pronunciation, Translation, Rang From Words as w
            Join Cards as c ON c.Name LIKE ?
            """, (card,))
            return cur.fetchall()

    def get_sentence_by_construction(self, construction) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            Select Sentence, Sentences.Translation  FROM Sentences JOIN Constructions
            ON Constructions.Construction LIKE ?
            """, (construction,))
            return cur.fetchall()

    def get_rule(self, name) -> list[tuple[str]]:
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            SELECT Rule FROM Rules WHERE Name LIKE ?
            """, (name,))
            return cur.fetchall()

    def add_new_word(self, spelling, pronunciation, translate, cartID, rang):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO words (Spelling, Pronunciation, Translation, CardID, Rang)
            VALUES (?, ?, ?, ?, ?)
            """, (spelling, pronunciation, translate, cartID, rang))

    def add_new_card(self, name):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Cards (Name) VALUES (?)
            """)

    def add_new_sentence(self, translation, constructionID, sentence):
        with SQLite.con as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Sentences (Translation, ConstructionID, Sentence)
            VALUES (?, ?, ?)
            """, (translation, constructionID, sentence))

    def add_new_construction(self, construction, translation):
        with SQLite as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO Constructions (Construction, Translation)
            VALUES (?, ?)
            """, (construction, translation,))
