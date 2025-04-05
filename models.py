from collections import UserDict
from datetime import datetime


class Field:
    """
    Base class for record fields.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Class for storing contact name. Required field.
    """

    pass


class Phone(Field):
    """
    Class for storing phone numbers. Has format validation (10 digits).
    """

    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False


class Birthday(Field):
    """
    Class for storing birthdays with validation.
    """

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """
    A class for storing contact information, including name, phones, and birthday.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        result = f"Contact: {self.name}, Phones: {phones}"
        if self.birthday:
            result += f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        return result

    def add_phone(self, phone_number):
        """
        Add a phone number to the contact.
        Raises a ValueError if the phone number already exists.
        """
        phone = Phone(phone_number)
        if phone in self.phones:
            raise ValueError(
                f"Phone {phone_number} already exists in contact {self.name}."
            )
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        """
        Remove a phone number from the contact.
        Raises a ValueError if the phone number is not found.
        """
        phone = Phone(phone_number)
        if phone not in self.phones:
            raise ValueError(
                f"Phone {phone_number} has not been found in contact {self.name}."
            )
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        """
        Edit a phone number in the contact.
        Raises a ValueError if the old phone number is not found.
        """
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)

        if old_phone_obj not in self.phones:
            raise ValueError(
                f"Phone {old_phone} has not been found in contact {self.name}."
            )

        index = self.phones.index(old_phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone_number):
        """
        Find a phone number in the contact.
        """
        phone = Phone(phone_number)
        if phone in self.phones:
            return phone
        return None

    def add_birthday(self, birthday):
        """
        Sets the birthday attribute by creating a new Birthday object.
        """
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """
    A class for storing and managing records.
    """

    def add_record(self, record: Record):
        """
        Adds a new record to the address book.
        Raises a ValueError if a record with the same name already exists.
        """
        name = str(record.name)
        if name in self.data:
            raise ValueError(f"Contact '{name}' already exists.")
        self.data[name] = record
        return f"Contact '{name}' has been added."

    def find(self, name: str):
        """
        Searches for a contact by name.
        Returns the Record object if found.
        Raises a KeyError if the contact does not exist.
        """
        record = self.data.get(name)
        if record:
            return record
        else:
            raise KeyError(f"Contact '{name}' has not been found.")

    def delete(self, name: str):
        """
        Deletes a contact by name.
        Raises a KeyError if the contact does not exist.
        """
        if name in self.data:
            del self.data[name]
            return f"Contact '{name}' has been successfully deleted."
        else:
            raise KeyError(f"Contact '{name}' not found.")

    def get_upcoming_birthdays(self):
        """
        Returns a list of contacts who have birthdays within the next 7 days.
        Raises a ValueError if a birthday date is invalid or improperly formatted.
        """
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                try:
                    birthday_this_year = record.birthday.value.replace(year=today.year)
                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(
                            year=today.year + 1
                        )
                    if (birthday_this_year - today).days < 7:
                        upcoming_birthdays.append(
                            f"{record.name}: {birthday_this_year.strftime('%d.%m.%Y')}"
                        )
                except ValueError as e:
                    raise ValueError(
                        f"Invalid birthday for contact '{record.name}': {e}"
                    )

        return upcoming_birthdays
