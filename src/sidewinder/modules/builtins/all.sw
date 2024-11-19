def all(iterable: Iterable[T]) -> bool:
    for element in iterable:
        if not element:
            return False
    return True
