from librarian.exceptions import EnvironmentVariableLoadException

import json
import os


def load_env_json(tag):
    """ Load a configuration dict from environment variable

    Args:
        tag (str): Environment variable to load

    Returns:
        Loaded dict from enc variable

    Raises:
        ValueError: if env variable with name tag is not defined
        EnvironmentVariableLoadException if data is not valid json
    """
    try:
        data_str = os.environ[tag]
        data = json.loads(data_str)
    except json.decoder.JSONDecodeError:
        raise EnvironmentVariableLoadException(
            f"Failed to load json from env var: {tag}"
        )
    return data


def parse_config_dicts(INPUT_CONFIG, CROSS_VALID_CONFIG,
                       LABEL_VALID_CONFIG,DATA_VALID_CONFIG,
                       LABEL_ACTOR_CONFIG, DATA_ACTOR_CONFIG):
    """ Parse configs into kwargs for librarian.create()

    Args:
        INPUT_CONFIG (dict):
        CROSS_VALID_CONFIG (dict):
        LABEL_VALID_CONFIG (dict):
        DATA_VALID_CONFIG  (dict):
        LABEL_ACTOR_CONFIG (dict):
        DATA_ACTOR_CONFIG  (dict):

    Returns (dict):
        Kwargs needed to create a librarian instance

    Raises:
        KeyError: if a needed tag was not found in config dict
    """
    return {
        # INPUT: These define which type of data is expected
        "DATA_TYPE": INPUT_CONFIG["type"],
        "DATA_TAG":  INPUT_CONFIG["tag"],

        # CROSS: these define validations for each label-data combination obtained
        "CROSS_VALID_TYPE": CROSS_VALID_CONFIG["validator"],
        "CROSS_VALID_ARGS": CROSS_VALID_CONFIG["args"],

        # LABEL: these define validations for each label object obtained
        "LABEL_VALID_TYPE": LABEL_VALID_CONFIG["validator"],
        "LABEL_VALID_ARGS": LABEL_VALID_CONFIG["args"],

        # DATA: these define validations for each data object obtained
        "DATA_VALID_TYPE": DATA_VALID_CONFIG["validator"],
        "DATA_VALID_ARGS": DATA_VALID_CONFIG["args"],

        # LABEL: these define actions for each label object obtained
        "LABEL_ACTOR_TYPE": LABEL_ACTOR_CONFIG["actor"],
        "LABEL_ACTOR_ARGS": LABEL_ACTOR_CONFIG["args"],

        # DATA: these define actions for each data object obtained
        "DATA_ACTOR_TYPE": DATA_ACTOR_CONFIG["actor"],
        "DATA_ACTOR_ARGS": DATA_ACTOR_CONFIG["args"],
    }


def load_configs_from_environment():
    """ Load Librarian service configuration from environment variables

    The environment variables are the following: DATA_TYPE, DATA_TAG,
    CROSS_VALID_CONFIG, LABEL_VALID_CONFIG, DATA_VALID_CONFIG,
    LABEL_ACTOR_CONFIG, DATA_ACTOR_CONFIG, DEBUG.

    Note, that if any of these is not found, the service will fail to start.

    Raises:
        ValueError: if env variable with name tag is not defined
        TypeError: if data in environment variable is not valid json
    """
    return {
        "INPUT_CONFIG":        load_env_json("INPUT_CONFIG"),
        "CROSS_VALID_CONFIG":  load_env_json("CROSS_VALID_CONFIG"),
        "LABEL_VALID_CONFIG":  load_env_json("LABEL_VALID_CONFIG"),
        "LABEL_ACTOR_CONFIG":  load_env_json("LABEL_ACTOR_CONFIG"),
        "DATA_VALID_CONFIG":   load_env_json("DATA_VALID_CONFIG"),
        "DATA_ACTOR_CONFIG":   load_env_json("DATA_ACTOR_CONFIG"),
    }



def load_configs_from_json(file):
    """ Load Librarian service configuration from local json config file

    See documentation for expected contents of the config file

    Args:
        file (str): json file containing the config values

    Raises:
        ValueError: if file given is not defined
        TypeError: if data in environment variable is not valid json
    """
    # Load the file:
    with open(file, 'rb') as f:
        config = json.load(f)
    return config


def load_test_configs():
    """ Load Librarian service configuration with dummy parameters

    Performs no validation on labels or data
    Prints information for both labels and data

    """
    return {
        "INPUT_CONFIG":       {"type": "json", "tag": ""},
        "CROSS_VALID_CONFIG": {"validator": "none", "args": []},
        "LABEL_VALID_CONFIG": {"validator": "none", "args": []},
        "DATA_VALID_CONFIG":  {"validator": "none", "args": []},
        "LABEL_ACTOR_CONFIG": {"actor": "print", "args": []},
        "DATA_ACTOR_CONFIG":  {"actor": "print", "args": []},
    }
