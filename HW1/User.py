class User:
    def __init__(self, name) -> None:
        self.__name = name
        self.__act_list = []

        self.get_name = lambda : self.__name
        self.get_act_list = lambda : self.__act_list