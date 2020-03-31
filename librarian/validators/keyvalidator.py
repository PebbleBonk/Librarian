from librarian.validators.validator import Validator
from librarian.validators.exceptions import ValidationError


class KeyValidator(Validator):
    """ Validator to check if an object contains all the defined values

        Args:
            keys (list): List of values to be found in the object validated
            strict (bool): Allow other keys to be present or not

        Returns (bool):
            Whether the validation was successful
    """
    def __init__(self, keys: list):
        if not isinstance(keys, list):
            raise InitialisationError("Invalid arguments")
        super().__init__()
        self.keys = set(keys)

    def __call__(self, obj):
        return set(obj.keys()) == self.keys