import re
import unicodedata

def slugify(text: str) -> str:
    """
    Convert `text` to a lowercase, hyphen-separated slug.
    Strips non-alphanumeric characters, collapses whitespace/punctuation into single hyphens.
    """
    # Normalize unicode characters (e.g. accents)
    text = unicodedata.normalize("NFKD", text)
    # Keep only letters, numbers, spaces, or hyphens
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    # Replace whitespace or repeated hyphens with a single hyphen
    text = re.sub(r"[-\s]+", "-", text).strip("-_")
    return text.lower()
