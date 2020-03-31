from librarian.actors import actors
from librarian.validators import validators, xvalidators


def describe_crossvalidator_options():
    """ Print options for cross validators and their arguments
    """
    print("* Currently supported options for",
          "LABEL_ACTOR_CONFIG and DATA_ACTOR_CONFIG:*", )
    for tag, validator in validators.items():
        print("'"+tag+"':", validator.describe())


def describe_validator_options():
    """ Print options for validators and their arguments
    """
    print("* Currently supported options for",
          "LABEL_VALID_CONFIG and DATA_VALID_CONFIG:*", )
    for tag, validator in validators.items():
        print("'"+tag+"'", validator.describe())


def describe_actor_options():
    """ Print options for actors and their arguments
    """
    print("* Currently supported options for CROSS_ACTOR_CONFIG: *")
    for tag, actor in actors.items():
        print("'"+tag+"'", actor.describe())


def describe_input_options():
    """ Print options for different inputs
    """
    print(
    """* Currently supported options for: *
    DATA_TYPE:
        'file': Expects a file. Reads the request.files field
        'json': Expects json dict. Reads the request.json field
        'base64': Expects base64 encoded string. Reads the request.form field

    DATA_TAG:
        This value can be anything. It is used to extract the data from
        the request, so it should match the data sent.
        NOTE: if the DATA_TYPE is 'json', then the DATA_TAG can be left
        empty to capture the entire content of request.json as data.

    """
    )