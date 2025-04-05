import pickle
from models import AddressBook


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
    If the file does not exist, returns a new empty AddressBook instance.

    Args:
        filename (str): The file name to load the data from. Defaults to 'addressbook.pkl'.

    Returns:
        AddressBook: The loaded address book object or a new one if the file is not found.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
