from collections import UserDict
from typing import Optional
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10:
            super().__init__(value)
        else:
            raise Exception("Phone must have 10 digits")

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        if not phones:
            self.phones = []
        elif isinstance(phones, str):
            self.phones = [Phone(phones)]
        elif isinstance(phones, list):
            self.phones = [i if isinstance(i, Phone) else Phone(i) for i in phones ]
        else:
            raise Exception("Unknown phones type")
        self.birthday = birthday

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone_to_find: str) -> Optional[str]:
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone.value
        return None

    def edit_phone(self, phone_to_edit: str, new_phone: str):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_edit:
                self.phones[index] = Phone(new_phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.get(name)

    def delete(self, name:str):
        self.pop(name)


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")