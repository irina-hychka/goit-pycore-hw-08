def input_error(func):
    """
    A decorator to handle input-related exceptions such as ValueError, KeyError, and IndexError.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: Wrapped function with error handling.
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


def parse_input(user_input):
    """
    Parses the user's input into a command and its arguments.

    Args:
        user_input (str): The input string from the user.

    Returns:
        tuple: A tuple containing the command (str) and a list of arguments (list).
    """
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args
