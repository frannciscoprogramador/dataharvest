from abc import ABC, abstractmethod


class SQL(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_profile_table(self):
        pass

    @abstractmethod
    def create_src_table(self):
        pass

    @abstractmethod
    def insert_src(self, id_profile, id_src):
        pass

    @abstractmethod
    def check_src_exists(self, id_src):
        pass

    @abstractmethod
    def insert_profile(self, id_profile):
        pass

    @abstractmethod
    def check_profile_exists(self, id_profile):
        pass
