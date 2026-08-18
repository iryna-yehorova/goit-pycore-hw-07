from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if  len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits")

        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value =  datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone):
        for recorded_phone in self.phones:
            if recorded_phone.value == phone:
                return recorded_phone
        return None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    def edit_phone(self, phone, new_phone):
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise ValueError("Phone not found")

        index = self.phones.index(found_phone)
        self.phones[index] = Phone(new_phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record (self, record):
        self.data[record.name.value] = record

    def find (self, name):
        return self.data.get(name)

    def delete (self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            days_difference = (birthday_this_year - today).days
            if 0 <= days_difference <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date = congratulation_date + timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date = congratulation_date + timedelta(days=1)

                upcoming_birthdays.append({
                    'name': record.name.value,
                    'congratulation_date': congratulation_date.strftime("%Y.%m.%d")
                })

        return upcoming_birthdays