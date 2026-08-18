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
def add_contact(info, contacts):
    name, phone = info
    name = name.lower()

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(info, contacts):
    name, phone = info
    name = name.lower()

    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return "Contact changed."


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved."

    contact_lines = []

    for name, phone in contacts.items():
        contact_lines.append(f"{name}: {phone}")

    return "\n".join(contact_lines)


@input_error
def phone_contact(args, contacts):
    name = args[0].lower()
    return f"{name}: {contacts[name]}"


def parse_input(user_input):
    parts = user_input.split()

    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


def main():
    contacts = {}
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
            print(add_contact(user_info, contacts))
        elif command == "change":
            print(change_contact(user_info, contacts))
        elif command == "phone":
            print(phone_contact(user_info, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")