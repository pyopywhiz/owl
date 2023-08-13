
from builder import IPerson


class PersonSingleton(IPerson):
    __instance = None

    @staticmethod
    def get_instance():
        if PersonSingleton.__instance == None:
            return PersonSingleton("Bob", 30)
        return PersonSingleton.__instance

    def __init__(self, name, age):
        if PersonSingleton.__instance != None:
            print("Can not create new instance")
        else:
            self.name = name
            self.age = age

            PersonSingleton.__instance = self

    @staticmethod
    def print_data():
        print(f"{PersonSingleton.__instance.name} {PersonSingleton.__instance.age}")