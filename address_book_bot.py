from collections import UserDict
from datetime import datetime
import pickle


def input_error(func):
    """
    A decorator to handle input errors.
    Handles ValueError, KeyError, and IndexError exceptions.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except KeyError:
            return "Error: contact not found."
        except IndexError as e:
            return str(e) or "Error: missing arguments."

    return inner


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


def save_data(book, filename="addressbook.pkl"):
    """
    Saves the address book object to a file using the pickle module.

    Args:
        book (AddressBook): The address book instance to be saved.
        filename (str): The file name to save the data to. Defaults to 'addressbook.pkl'.

    Returns:
        None
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Loads the address book object from a file using the pickle module.

    Params:
        filename (str): The file name to load the data from. Defaults to 'addressbook.pkl'.

    Returns:
        AddressBook: The loaded address book object or a new one if the file is not found.
        If the file does not exist, returns a new empty AddressBook instance.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def parse_input(user_input):
    """
    Parses the user's input into a command and arguments.
    Returns the command in lowercase and the list of arguments.
    """
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(args, book: AddressBook):
    """
    Adds a new contact with a phone number to the address book.
    If the contact already exists, adds a new phone to that contact.
    Raises ValueError if arguments are invalid or phone format is incorrect.
    """
    if len(args) != 2:
        raise ValueError("Provide exactly two arguments: name and phone.")
    name, phone = args
    try:
        # Validate phone format
        phone_obj = Phone(phone)
    except ValueError as e:
        raise ValueError(str(e))

    try:
        # Try to find existing contact
        record = book.find(name)
        record.add_phone(phone_obj.value)
        return "Phone added to existing contact."
    except KeyError:
        # Create new contact if not found
        record = Record(name)
        record.add_phone(phone_obj.value)
        book.add_record(record)
        return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    """
    Edits a contact's existing phone number to a new one.
    Raises ValueError if arguments are missing or the old phone number doesn't exist.
    """
    if len(args) < 3:
        raise ValueError("Provide name, old phone, and new phone.")
    name, old_phone, new_phone = args[:3]
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for contact '{name}'."


@input_error
def remove_contact(args, book: AddressBook):
    """
    Removes a contact entirely from the address book by name.
    Raises ValueError if name is missing.
    """
    if len(args) != 1:
        raise ValueError("Provide exactly one name to delete the contact.")

    name = args[0]
    book.delete(name)
    return f"Contact '{name}' has been deleted."


@input_error
def show_phone(args, book: AddressBook):
    """
    Shows all phone numbers associated with the given contact name.
    Raises ValueError if name is missing or no phones are found.
    """
    if len(args) != 1:
        raise ValueError("Please provide exactly one name.")
    name = args[0]
    record = book.find(name)
    if not record.phones:
        return f"No phone numbers found for contact '{name}'."
    phones = ", ".join(p.value for p in record.phones)
    return f"Phone numbers for '{name}': {phones}"


@input_error
def show_all(book: AddressBook):
    """
    Displays all contacts in the address book.
    Returns a message if the address book is empty.
    """
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """
    Adds a birthday to the specified contact.
    Raises ValueError if arguments are missing or birthday format is invalid.
    """
    if len(args) < 2:
        raise ValueError("Provide name and birthday.")
    name, birthday = args[:2]
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """
    Shows the birthday for the specified contact.
    Raises IndexError if name is not provided.
    """
    if not args:
        raise IndexError("Please enter a name.")
    record = book.find(args[0])
    return (
        record.birthday.value.strftime("%d.%m.%Y")
        if record and record.birthday
        else "No birthday found."
    )


@input_error
def birthdays(book: AddressBook):
    """
    Displays a list of upcoming birthdays within the next 7 days.
    If no upcoming birthdays, returns a message to notify about it.
    """
    upcoming = book.get_upcoming_birthdays()
    return (
        "Upcoming Birthdays:\n" + "\n".join(upcoming)
        if upcoming
        else "No upcoming birthdays."
    )


def main():
    # book = AddressBook()
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "delete":
            print(remove_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
