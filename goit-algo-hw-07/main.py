import datetime
import time

from classes import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, address_book):
    name, phone = args
    address_book.add_record(Record(name, phone))
    return "Contact added."


@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.get(name)
    if record:
        return record
    return 'Not found'


@input_error
def change_phone(args, address_book):
    name, phone = args
    record: Record = address_book.get(name)
    if record:
        record.phones.clear()
        record.phones = [Phone(phone)]
        return "Phone changed"
    return "Not found"


@input_error
def all_phones(args, address_book: AddressBook):
    records = ""
    for record in address_book.values():
        records += str(record)+"\n"
    return records


@input_error
def add_birthday(args, address_book):
    name, birthday = args
    record = address_book.get(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday was changed"
    return "Not found"


@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.get(name)
    if record:
        return record.birthday
    return "Not found"


@input_error
def birthdays(args, address_book):
    birthdays_string = ""
    for record in address_book.values():
        birthday = datetime(
            year=datetime.now().year,
            month=record.birthday.value.month,
            day=record.birthday.value.day
        )

        if birthday.timestamp() - time.time() <= (3600 * 24) * 7:
            birthdays_string += f"Contact name: {record.name}, Birthday {record.birthday}\n"
    return birthdays_string


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "all":
            print(all_phones(args, book), end="")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book), end="")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
