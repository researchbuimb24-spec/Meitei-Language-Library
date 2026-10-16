"""Custom exceptions for the meitei_lang library."""


class MeiteiLangError(Exception):
    """Base exception for all meitei_lang errors."""
    pass


class WordNotFoundError(MeiteiLangError):
    """Raised when a requested word is not found in the vocabulary dataset."""
    pass


class BookNotFoundError(MeiteiLangError):
    """Raised when a requested book is not found in the collection."""
    pass


class ChapterNotFoundError(MeiteiLangError):
    """Raised when a requested chapter number does not exist for a given book."""
    pass


class SongNotFoundError(MeiteiLangError):
    """Raised when a requested song record is not found."""
    pass


class LyricsNotAvailableError(MeiteiLangError):
    """Raised when lyrics are requested for a song where lyrics cannot be provided."""
    pass


class DataLoadError(MeiteiLangError):
    """Raised when a packaged dataset file cannot be loaded or is corrupted."""
    pass


class ValidationError(MeiteiLangError):
    """Raised when input text or dataset schema fails validation."""
    pass
