import re


def sanitize_filename(name: str, max_len: int = 50) -> str:
    if not name:
        return "unknown_user"

    name = re.sub(r'[\\/*?:"<>|]', "", name)

    name = name.replace(" ", "_")

    name = name.strip('._')

    if len(name) > max_len:
        name = name[:max_len]

    if not name:
        return "sanitized_user"

    return name
