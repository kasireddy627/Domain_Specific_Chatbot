def trim_message(message: str, max_chars: int = 3000) -> str:
    if len(message) > max_chars:
        return message[:max_chars]
    return message