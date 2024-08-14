from abc import ABC, abstractmethod


class Skeleton(ABC):

    @abstractmethod
    def get_all_words(self) -> list[tuple[str]]:
        raise NotImplementedError


    @abstractmethod
    def get_all_cards(self) -> list[tuple[str]]:
        raise NotImplementedError


    @abstractmethod
    def get_all_sentences(self) -> list[tuple[str]]:
        raise NotImplementedError


    @abstractmethod
    def get_all_construction(self) -> list[tuple[str]]:
        raise NotImplementedError

    @abstractmethod
    def get_words_by_card(self, card) -> list[tuple[str]]:
        raise NotImplementedError

    @abstractmethod
    def get_sentence_by_construction(self, construction) -> list[tuple[str]]:
        raise NotImplementedError

    @abstractmethod
    def get_rule(self, name) -> list[tuple[str]]:
        raise NotImplementedError

    @abstractmethod
    def add_new_word(self, spelling, pronunciation, translate, cartID, rang):
        raise NotImplementedError

    @abstractmethod
    def add_new_card(self, name):
        raise NotImplementedError

    @abstractmethod
    def add_new_sentence(self, translation, constructionID):
        raise NotImplementedError

    @abstractmethod
    def add_new_construction(self, construction, translation):
        raise NotImplementedError

