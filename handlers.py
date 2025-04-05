from models import Phone, Record, AddressBook
from utils import input_error


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
    if record.birthday:
        record.add_birthday(birthday)
        return "Birthday updated."
    else:
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
