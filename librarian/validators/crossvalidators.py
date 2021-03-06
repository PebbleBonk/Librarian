from librarian.validators.validator import Validator, CompositeValidator
from librarian.validators.exceptions import ValidationError, InitialisationError


class DummyCrossValidator(Validator):
    """ A dummy cross validator: does nothing, i.e. passes everything.

    Great for debugging. Takes no arguments.

    Returns (bool):
        Always True
    """
    def __init__(self):
        self.description = "Does nothing. Passes everything."
        super().__init__()
        pass

    def __call__(self, x, y):
        return True



class MacthFileNames:
    """ Cross validator to check if two objects contain same filenames

        Tries to access "filenames" from the data with .get()
        Takes no arguments.

        Returns (bool):
            True if both are accessible and identical
    """
    def __init__(self):
        self.description = "Checks for matching filenames."
        super().__init__()
        pass

    def __call__(self, x, y):
        fn1 = x.get('filename', False)
        fn2 = y.get('filename', False)

        return (fn1 and f2) and fn1 == fn2


class CompositeCrossValidator(CompositeValidator):
    def __init__(self, *xvalidators):
        self.description = "Composed CrossValidator"
        super().__init__(*xvalidators)

    def __call__(self, x, y):
        return all([validate(x,y) for validate in self.validators])

    def __str__(self):
        string = self.__class__.__name__ +" with Cross Validators:\n"
        for validator in self.validators:
            string += "\t"+str(validator).replace('\n', '\n\t')
        return string

