def calculate_average(numbers):
    if not numbers:
        return 0
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1
    return total / count if count > 0 else 0


def get_user_name(user):
    if user is None:
        return None
    if not isinstance(user, dict):
        return None
    name = user.get("name")
    return name.upper() if name is not None else None