class SportActivty:
    def __init__(self, author, name, time, place) -> None:
        self.__author = author
        self.__name = name
        self.__time = time
        self.__place = place

        self.get_author = lambda:self.__author
        self.get_name = lambda: self.__name
        self.get_time = lambda: self.__time
        self.get_place = lambda: self.__place
