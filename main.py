from address_book import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return 'Give me a user name please'
        except KeyError:
            return 'Contact not found'

    return inner


@input_error
def add_contact(info, book):
    name, phone = info
    name = name.lower()
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(info, book):
    name, old_phone, phone = info
    name = name.lower()

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, phone)
    return "Contact changed."


@input_error
def show_all(book):
    print("Here is all phone list")
    for record in book.values():
        print(record)

@input_error
def phone_contact(args, book):
    name = args[0].lower()

    record = book.find(name)
    if record is None:
        raise KeyError

    return record.phones


@input_error
def add_birthday(args, book):
    name, birthday = args

    record = book.find(name.lower())
    record.add_birthday(birthday)
    return 'Birthday added.'


@input_error
def show_birthday(args, book):
    record = book.find(args)
    return f"{record.name.upper()}'s birthday is {record.birthday}"


@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()


def parse_input(user_input):
    parts = user_input.split()

    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, user_info = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(user_info, book))
        elif command == "change":
            print(change_contact(user_info, book))
        elif command == "phone":
            print(phone_contact(user_info, book))
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            print(add_birthday(user_info, book))
        elif command == "show-birthday":
            print(show_birthday(user_info, book))
        elif command == "birthdays":
            print("Here is th list of upcoming birthdays")
            birthdays(book)
        else:
            print("Invalid command.")