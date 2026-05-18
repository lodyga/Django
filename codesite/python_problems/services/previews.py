import binarytree
from python_problems.models import ProblemType


def is_grid_shape(data):
    if not data:
        return

    for row in data:
        if len(row) != len(data[0]):
            return
        if not row:
            return

    return True


def draw_grid(data, parameter_name):
    if not is_grid_shape(data):
        return

    rows = len(data)
    cols = len(data[0])
    chars = {str(char) for line in data for char in line}
    char_map = {}

    if all(char.isalpha() for char in chars):
        return

    match len(chars):
        case 1 | 2 | 3:
            char_map = {
                "-1": "█",
                "0": "·",
                "1": "■",
                "2": "X",
                "2147483647": "∞",
            }
        case _:
            char_map = {char: char for char in chars}
            char_map["-1"] = "█"

    grid = """┌""" + "─" * (cols*2 + 1) + "┐\n"

    for line in data:
        grid_line = "".join(
            char_map.get(str(char), "J")
            for char in line
        )
        grid = grid + "│ " + " ".join(grid_line) + " │\n"

    grid = grid + """└""" + "─" * (cols*2 + 1) + "┘"

    return (parameter_name, grid)


def draw_tree(data, parameter_name):
    bt = binarytree.build2(data).__str__()
    parameter_name = parameter_name or "root"
    return (parameter_name, bt)


def unpack_linked_list_payload(data):
    if not isinstance(data, dict):
        return data, -1

    values = None
    for key in ("values", "nodes", "list"):
        if key in data:
            values = data[key]
            break

    cycle_position = -1
    for key in ("cycle_position", "cyclePosition", "pos"):
        if key in data:
            cycle_position = data[key]
            break

    if values is None:
        return data, -1

    if not isinstance(cycle_position, int):
        cycle_position = -1

    return values, cycle_position


def draw_linked_list(data, parameter_name):
    values, cycle_position = unpack_linked_list_payload(data)

    if not isinstance(values, list):
        preview = str(data)
        return (parameter_name, preview)

    preview = ("(" + ") -> (".join(map(str, values)) + ")") if values else "null"

    if 0 <= cycle_position < len(values):
        preview += f" -> ↺ index {cycle_position} ({values[cycle_position]})"

    return (parameter_name, preview)


def draw_list(heights, parameter_name):
    if not heights:
        return ""

    fill = "█"
    max_height = max(heights)
    lines = []

    for level in range(max_height, 0, -1):
        row = f"{level:>2} | "

        for h in heights:
            if h >= level:
                row += f"{fill} "
            else:
                row += "  "

        lines.append(row.rstrip())

    axis = "   +" + "-" * (2 * len(heights) + 1)
    indexes = "     " + " ".join(str(i) for i in range(len(heights)))

    lines.append(axis)
    lines.append(indexes)

    return (parameter_name, "\n".join(lines))


def draw_ascii(data, problem_type, parameter_name, parameter_type):
    """
    █▓▒░#║╬■⬛🧱~≈∼≋≀·○🌊💧■▲◆●⬤⛰GO⊙✦★
    """
    match parameter_type:
        case ProblemType.BINARY_TREE:
            return draw_tree(data, parameter_name)
        case ProblemType.LINKED_LIST:
            return draw_linked_list(data, parameter_name)
        case "list[int]":
            return draw_list(data, parameter_name)
        # todo grid?
        case "list[list[int]]" | "grid":
            return draw_grid(data, parameter_name)

    if problem_type == ProblemType.BINARY_TREE and isinstance(data, list):
        bt = binarytree.build2(data).__str__()
        return (parameter_name, bt)

    elif problem_type == ProblemType.LINKED_LIST and isinstance(data, list):
        return draw_linked_list(data, parameter_name)

    # for grid/matrix/board-like data
    elif problem_type not in (ProblemType.BINARY_TREE, ProblemType.LINKED_LIST) and data and isinstance(data, list) and isinstance(data[0], list):
        return draw_grid(data, parameter_name)
