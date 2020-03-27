from librarian.librarian import launch_librarian

from librarian.actors import actors
from librarian.validators import validators, xvalidators

# import config
import json
import fire
import sys


def describe_crossvalidator_options():
    """ Print options for cross validators and their arguments
    """
    for tag, validator in validators.items():
        print("'"+tag+"':", validator.describe())

def describe_validator_options():
    """ Print options for validators and their arguments
    """
    for tag, validator in validators.items():
        print("'"+tag+"'", validator.describe())


def describe_actor_options():
    """ Print options for actors and their arguments
    """
    for tag, actor in actors.items():
        print("'"+tag+"'", actor.describe())


def _load_env_json(tag):
    """ Load a configuration dict from environment variable

    Args:
        tag (str): Environtment variable to load

    Returns:
        Loaded dict from enc variable

    Raises:
        ValueError: if env variable with name tag is not defined
        TypeError: if data in environment variable is not valid json
    """
    data_str = os.environ[tag]
    return json.loads(data_str)


def launch_with_env(debug=True):
    """ Launch Librarian service with parameters from environment variables

    Args:
        debug (bool): start the service with Flask debugging (default:True)

    Raises:
        ValueError: if env variable with name tag is not defined
        TypeError: if data in environment variable is not valid json
    """
    DATA_TYPE = os.environ.get("DATA_TYPE", "{}")
    DATA_TAG = os.environ.get("DATA_TAG", "{}")

    CROSS_VALID_CONFIG =  _load_env_json("CROSS_VALID_CONFIG")
    LABEL_VALID_CONFIG =  _load_env_json("LABEL_VALID_CONFIG")
    LABEL_ACTOR_CONFIG =  _load_env_json("LABEL_ACTOR_CONFIG")
    DATA_VALID_CONFIG =  _load_env_json("DATA_VALID_CONFIG")
    DATA_ACTOR_CONFIG =  _load_env_json("DATA_ACTOR_CONFIG")

    launch(DATA_TYPE, DATA_TAG, CROSS_VALID_CONFIG, LABEL_VALID_CONFIG,
           DATA_VALID_CONFIG, LABEL_ACTOR_CONFIG, DATA_ACTOR_CONFIG, debug)


def launch_with_config_file(file, debug=True):
    """ Launch Librarian service with parameters from local json config file

    See documentation for expected contents of the config file

    Args:
        file (str): json file containing the config values
        debug (bool): start the service with Flask debugging enabled

    Raises:
        ValueError: if file given is not defined
        TypeError: if data in environment variable is not valid json
    """
    # Load the file:
    with open(file, 'rb') as f:
        config = json.load(f)
    launch(**config, DEBUG=debug)


def launch_with_defaults(debug=True):
    """ Launch Librarian service with default parameters

    Performs no validation on labels or data
    Prints information for both labels and data

    Args:
        debug (bool): start the service with Flask debugging (default:True)
    """
    default_validator_config = {"validator": "none", "args": []}
    default_actor_config = {"actor": "print", "args": []}
    launch('json', 'data', default_validator_config,
        default_validator_config, default_validator_config,
        default_actor_config, default_actor_config, debug
    )


def launch(DATA_TYPE, DATA_TAG, CROSS_VALID_CONFIG, LABEL_VALID_CONFIG,
           DATA_VALID_CONFIG, LABEL_ACTOR_CONFIG, DATA_ACTOR_CONFIG, DEBUG):
    # CROSS: these define validations for each label-data combination obtained
    print(CROSS_VALID_CONFIG)
    CROSS_VALID_TYPE = CROSS_VALID_CONFIG["validator"]
    CROSS_VALID_ARGS = CROSS_VALID_CONFIG["args"]

    # LABEL: these define validations for each label object obtained
    LABEL_VALID_TYPE = LABEL_VALID_CONFIG["validator"]
    LABEL_VALID_ARGS = LABEL_VALID_CONFIG["args"]

    # DATA: these define validations for each data object obtained
    DATA_VALID_TYPE = DATA_VALID_CONFIG["validator"]
    DATA_VALID_ARGS = DATA_VALID_CONFIG["args"]

    # LABEL: these define actions for each label object obtained
    LABEL_ACTOR_TYPE = LABEL_ACTOR_CONFIG["actor"]
    LABEL_ACTOR_ARGS = LABEL_ACTOR_CONFIG["args"]

    # DATA: these define actions for each data object obtained
    DATA_ACTOR_TYPE = DATA_ACTOR_CONFIG["actor"]
    DATA_ACTOR_ARGS = DATA_ACTOR_CONFIG["args"]


    # Setup validators and actors:
    try:
        lbl_valid = validators[LABEL_VALID_TYPE](*LABEL_VALID_ARGS)
        data_valid = validators[DATA_VALID_TYPE](*DATA_VALID_ARGS)
        cross_valid = xvalidators[CROSS_VALID_TYPE](*CROSS_VALID_ARGS)
    except TypeError as e:
        raise Exception("Invalid Validator initialisation: "+str(e))

    try:
        lbl_actor = actors[LABEL_ACTOR_TYPE](*LABEL_ACTOR_ARGS)
        data_actor = actors[DATA_ACTOR_TYPE](*DATA_ACTOR_ARGS)
    except TypeError as e:
        raise Exception("Invalid Actor initialisation: "+str(e))


    launch_librarian(
        datatype=DATA_TYPE, datatag=DATA_TAG,
        label_validator=lbl_valid, label_actor=lbl_actor,
        data_validator=data_valid, data_actor=data_actor,
        cross_validator=cross_valid,
        debug=DEBUG,
    )

if __name__ == "__main__":
    fire.Fire()