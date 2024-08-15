from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Word:
    word_id: str = None
    spelling: str = None
    pronunciation: str = None
    translation: str = None
    card_id: str = None
    rang: str = None
    time_repeat: str = None


@dataclass
class Card:
    card_id: str = None
    name: str = None


@dataclass
class Sentence:
    sentence_id: str = None
    construction_id: str = None
    sentence: str = None
    construction: str = None
    translation: str = None


@dataclass
class Construction:
    construction_id: str = None
    construction: str = None
    translation: str = None


@dataclass
class Rule:
    rule_id: str = None
    rule: str = None
    name: str = None


class DatabaseInterface(ABC):

    @abstractmethod
    def get_all_words(self) -> list[Word]:
        raise NotImplementedError

    @abstractmethod
    def get_all_cards(self) -> list[Card]:
        raise NotImplementedError

    @abstractmethod
    def get_all_sentences(self) -> list[Sentence]:
        raise NotImplementedError

    @abstractmethod
    def get_all_construction(self) -> list[Construction]:
        raise NotImplementedError

    @abstractmethod
    def get_all_name_rules(self) -> list[Rule]:
        raise NotImplementedError

    @abstractmethod
    def get_words_by_card(self, card) -> list[Word]:
        raise NotImplementedError

    @abstractmethod
    def get_sentence_by_construction(self, construction) -> list[Sentence]:
        raise NotImplementedError

    @abstractmethod
    def get_rule(self, name) -> list[Rule]:
        raise NotImplementedError

    @abstractmethod
    def get_id_by_name_card(self, name) -> list[Card]:
        raise NotImplementedError

    @abstractmethod
    def get_id_by_construction(self, construction) -> list[Construction]:
        raise NotImplementedError

    @abstractmethod
    def get_word_for_time_repeat(self) -> list[Word]:
        raise NotImplementedError

    @abstractmethod
    def add_new_word(self, spelling, pronunciation, translate, cart_id, rang, time_repeat):
        raise NotImplementedError

    @abstractmethod
    def add_new_card(self, name):
        raise NotImplementedError

    @abstractmethod
    def add_new_sentence(self, translation, construction_id, sentence):
        raise NotImplementedError

    @abstractmethod
    def add_new_construction(self, construction, translation):
        raise NotImplementedError

    @abstractmethod
    def set_time_for_word(self, word_id, time_repeat, rang):
        raise NotImplementedError

    @abstractmethod
    def save_rule(self, name, rule):
        raise NotImplementedError
