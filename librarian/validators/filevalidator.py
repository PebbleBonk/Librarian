from librarian.validators.validator import Validator
from librarian.validators.exceptions import ValidationError, InitialisationError


class FileValidator(Validator):
    """ Validator to check the type of a file

        Currently imply checks the filename for the extension with a
        simple split.
        TODO: Replace with basename for more robustness

        Args:
            filetypes (list): List of accepted filetypes as strings

        Returns (bool):
            Whether the validation was successful
    """
    def __init__(self, filetypes: list):
        super().__init__()
        self.filetypes = filetypes

    def __call__(self, obj):
        return any([obj.filename.endswith(ft) for ft in self.filetypes])