import logging

logger = logging.getLogger(__name__)


def issubclass_safe(cls, classinfo):
    """Check if a class is a subclass of another class.
    Some classes like list, dict, etc. returns true when checked inspect.isclass
    however, they raise TypeError when checked with issubclass.
    """
    try:
        return issubclass(cls, classinfo)
    except TypeError:
        return False