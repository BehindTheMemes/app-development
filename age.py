def is_adult(age: int) -> bool:
    if age < 0:
        raise ValueError("возраст не может быть < 0")
    return age >= 18