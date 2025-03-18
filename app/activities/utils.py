def is_valid_depth(activity, max_depth=3):
    """
    Проверяет, что уровень вложенности не превышает max_depth.
    """
    depth = 0

    while activity.parent is not None:
        depth += 1
        if depth > max_depth:
            return False

        activity = activity.parent

    return True
