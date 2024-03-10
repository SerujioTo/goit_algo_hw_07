from datetime import datetime
from collections import UserDict
from typing import Optional


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except Exception as e:
            raise ValueError(f"Invalid date: {repr(e)}")
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid():
            raise ValueError("Phone number isnt valid it must have digits only and 10 digits")

    def is_valid(self):
        try:
            int(self.value)
            assert len(self.value) == 10, "Phone number isnt 10 digits long"
            return True
        except (ValueError, AssertionError):
            return False

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def set_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone_to_find: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        return None

    def edit_phone(self, phone_to_edit: str, new_phone: str):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_edit:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError("Phone isnt in record to edit")

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

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
    john_record.edit_phone("9876897561", "8956958768") # < Value error

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