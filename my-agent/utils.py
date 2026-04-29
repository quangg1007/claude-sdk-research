def calculate_average(numbers):
    """Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The average (mean) of the numbers as a float. Returns 0 if the list is empty.
    """
    if not numbers:
        return 0
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    return total / count if count > 0 else 0


def get_user_name(user):
    """Extract and uppercase the user's name from a user dictionary.

    Args:
        user: A dictionary containing user information with a 'name' key,
              or None.

    Returns:
        The user's name in uppercase as a string, or None if:
        - user is None
        - user is not a dictionary
        - the 'name' key is missing or None
    """
    if user is None:
        return None
    if not isinstance(user, dict):
        return None
    name = user.get("name")
    return name.upper() if name is not None else None