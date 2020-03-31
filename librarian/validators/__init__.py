from librarian.validators import validator
from librarian.validators import crossvalidators
from librarian.validators import filevalidator
from librarian.validators import typevalidator
from librarian.validators import keyvalidator
from librarian.validators import imagevalidator



validators = {
    'file': filevalidator.FileValidator,
    'type': typevalidator.TypeValidator,
    'key':  keyvalidator.KeyValidator,
    'img': imagevalidator.ImageValidator,
    'none': validator.DummyValidator
}

xvalidators = {
    'none': crossvalidators.DummyCrossValidator,
    'fname': crossvalidators.MacthFileNames
}



def configure_validator(config):
    """ Create a validator using configuration

        All the different validators given in config are composed into
        one single Validator. The validations are done in order given.

        Args:
            config (list): List of config dicts to create the validator

        Returns (Validator):
            Validator class to validate data / labels.

        Raises:
            KeyError if configuration key is not found in options.
    """
    # No validato used, return just a dummy:
    if len(config) == 0:
        return validator.DummyValidator()

    # Single validator
    elif len(config) == 1:
        config = config[0]
        tag = config['validator']
        args = config['args']
        return validators[tag](*args)

    # Compose a validator using multiple validators:
    else:
        composite = validator.CompositeValidator()
        for c in config:
            tag = c['validator']
            args = c['args']
            composite += validators[tag](*args)
        return composite


def configure_xvalidator(config):
    """ Create a cross validator using configuration

        All the different validators given in config are composed into
        one single Validator. The validations are done in order given.

        Args:
            config (list): List of config dicts to create the validator

        Returns (Validator):
            Validator class to validate data / labels.

        Raises:
            KeyError if configuration key is not found in options.
    """
    # No validato used, return just a dummy:
    if len(config) == 0:
        return crossvalidators.DummyCrossValidator()

    # Single validator
    elif len(config) == 1:
        config = config[0]
        tag = config['validator']
        args = config['args']
        return xvalidators[tag](*args)

    # Compose a validator using multiple validators:
    else:
        composite = crossvalidators.CompositeCrossValidator()
        for c in config:
            tag = c['validator']
            args = c['args']
            composite += xvalidators[tag](*args)
        return composite

