from slugify import slugify as pyslugify


def slugify(txt: str, length: int = 128) -> str:
    """Slugify a string

    Thin wrapper around python-slugify.

    Args:
      length: int: Maximum length of the slug (Default value = 128)

    Returns:
      A string converted to a slug

    """
    return pyslugify(txt, max_length=length, word_boundary=True)
