# import inspect


class Validator:
    """ Base class for all Validators. Cannot work by itself.

    The inheriting classes must implement the __init__ and __call__
    methods.
    """
    def __init__(self):
        pass

    def __call__(self, obj):
        raise NotImplementedError("Inherited method not implemented")

    def __str__(self):
        setup = self.__class__.__name__ +" with setup:"
        for var, val in vars(self).items():
            setup += f"\n\t{var}: {val}"
        return setup

    def __repr__(self):
        return str(self).replace('\n', ', ').replace('\t', '')

    @classmethod
    def describe(cls):
        return ''.join([cls.__name__, '\n', cls.__doc__.strip('\n')])
        # NOTE: Cleaner and more descriptive with docstrings:
        # signature = inspect.signature(cls.__init__)
        # for name, param in signature.parameters.items():
        #     print(f'\t{name} ({param.annotation.__name__})')


class CompositeValidator:
    """ Compose a combination of several validators

        Checks the object agains every validator

        Args:
            *validators: validators to compose the validator from
    """
    def __init__(self, *validators):
        self.validators = list(validators) if validators is not None else []

    def  __add__(self, other):
        self.validators.append(other)
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __call__(self, obj):
        return all([validate(obj) for validate in self.validators])

    def __str__(self):
        string = self.__class__.__name__ +" with Validators:"
        for validator in self.validators:
            string += "\n\t"+str(validator).replace('\n', '\n\t')
        return string

    def __repr__(self):
        return str(self).replace('\n', ', ').replace('\t', '').strip()


class DummyValidator(Validator):
    """ A dummy validator: does nothing, i.e. passes everything.

    Great for debugging. Takes no arguments.
    """
    def __init__(self):
        self.description = "Does nothing. Passes everything."
        super().__init__()

    def __call__(self, obj):
        return True