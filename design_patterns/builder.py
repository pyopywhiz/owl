class Person:
    def __init__(self):
        self.name = None
        self.age = None
        self.address = None

    def __str__(self):
        return f"{self.name} {self.age} {self.address}"


class PersonBuilder:

    def __init__(self, person=None):
        self.person = person if person else Person()

    def set_name(self, name):
        self.person.name = name
        return self

    def set_age(self, age):
        self.person.age = age
        return self

    def set_address(self, address):
        self.person.address = address
        return self

    def build(self):
        return self.person


builder = PersonBuilder()
person = builder.build()
print(person)

builder2 = PersonBuilder()
person2 = builder2.\
    set_name("patrick").\
    set_age(30).\
    build()
print(person2)


builder3 = PersonBuilder(person2)
person3 = builder3.\
    set_address("My dinh").\
    build()
print(person3)

