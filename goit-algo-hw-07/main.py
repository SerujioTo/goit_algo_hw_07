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
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def show_phones(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return ', '.join(p.value for p in record.phones)
    return 'Not found'


@input_error
def change_phone(args, address_book):
    name, old_phone, phone = args
    record: Record = address_book.find(name)
    if record:
        record.edit_phone(old_phone, phone)
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
    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday was changed"
    return "Not found"


@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return record.birthday
    return "Not found"


@input_error
def birthdays(args, address_book):
    birthdays_string = ""
    for record in address_book.values():
        if record.birthday is None:
            continue
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
            print(show_phones(args, book))
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
