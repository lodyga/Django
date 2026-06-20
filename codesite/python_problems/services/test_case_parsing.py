import json
from .languages import get_language_name


def serialize_cpp(items):
    # Serialize for C++ like json.dumps or JSON.stringify.
    """
    [2, 7, 11, 15] => '{2, 7, 11, 15}'
    """
    if isinstance(items, list):
        serialized = [serialize_cpp(item)
                      for item in items]

        return "{" + ", ".join(serialized) + "}"

    return json.dumps(items)


def serialize_java(items):
    # Serialize for C++ like json.dumps or JSON.stringify.
    """
    [2, 7, 11, 15] => 'new int[] {2, 7, 11, 15}'
    """
    if isinstance(items, list):
        serialized = [serialize_cpp(item)
                      for item in items]

        return "new int[] {" + ", ".join(serialized) + "}"

    return json.dumps(items)


def serialize(value, language) -> str:
    """
    [2, 7, 11, 15] => '[2, 7, 11, 15]'
    """
    language_name = get_language_name(language)

    match language_name:
        case "Python":
            return repr(value)
        case "JavaScript":
            return json.dumps(value)
        case "Cpp":
            return serialize_cpp(value)
        case "Java":
            return serialize_java(value)
        case _:
            return ""


def get_field(data, key):
    if isinstance(data, dict):
        return data[key]

    elif isinstance(data, list):
        idx_map = {
            "inputs": 0,
            "expected": 1 if len(data) == 2 else 2,
            "operations": 0,
            "arguments": 1,
        }
        return data[idx_map[key]]
