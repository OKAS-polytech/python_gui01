from dataclasses import dataclass

@dataclass
class Memo:
    """A simple data class to hold memo information."""
    id: str
    title: str
    content: str
    timestamp: str
