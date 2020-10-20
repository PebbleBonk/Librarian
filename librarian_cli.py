from librarian import validators
from librarian import actors
from librarian import exceptions as libex
from librarian import describers
from librarian import factory
from librarian import utils

from dotenv import load_dotenv

# import config
# import json
import fire
import os


def describe(validators=False, actors=False, inputs=False, xvalidators=False):
    """ Print information of options and arguments """
    if not (validators or actors or inputs or xvalidators):
        # TODO: Better default print
        print("Options: 'xvalidators', 'validators', 'actors', 'inputs")
    if inputs:
        describers.describe_input_options()
    if validators:
        describers.describe_validator_options()
    if xvalidators:
        describers.describe_crossvalidator_options()
    if actors:
        describers.describe_actor_options()



def launch(dotenv=None, json=None, test=False, port=5000, debug=True):
    """ Launches a Librarian instance as a flask app

    Provides different options to load to configuration for the instance:
    using environmental variables, using a .env file, using a config json
    and using a dummy setup.

    If none of the config options are provided, the app will be created
    with environmental variables.

    Args:
        dotenv (str): .env file to load for configuration
        json   (str): json file to load for configuration
        test  (bool): create the service with dummy setup
        port   (int): Port to assign to the created Flask app
        debug (bool): Start the Flask app in debug mode

    """

    app = create(dotenv, json, test)

    # Something went wrong during creation:
    if app is None:
        return

    if debug:
        app.run(host="0.0.0.0", debug=True, port=port)
    else:
        app.run(port=port)


def create(dotenv=False, json=False, test=False):
    """ Creates a Librarian instance as a flask app

    Provides different options to load to configuration for the instance:
    using environmental variables, using a .env file, using a config json
    and using a dummy setup.

    If none of the config options are provided, the app will be created
    with environmental variables.

    Args:
        dotenv (str): .env file to load for configuration
        json   (str): json file to load for configuration
        test  (bool): create the service with dummy setup

    Returns (flask.app):
        An app ready to run.

    """
    if test:
        config_kwargs = utils.load_test_configs()

    elif json:
        try:
            config_kwargs = utils.load_configs_from_json(json)
        except FileNotFoundError as e:
            _fail_config(f'Defined config json file not found: {e}')
            return
        except ValueError as e:
            _fail_config(f'Defined config json is not valid: {e}')
            return

    else:
        if dotenv:
            load_dotenv(dotenv_path=dotenv)
        try:
            config_kwargs = utils.load_configs_from_environment()
        except KeyError as e:
            _fail_config(f'Environment variable not set: {e}')
            return
        except libex.EnvironmentVariableLoadException as e:
            _fail_config(f'Error loading environment configs: {e}')
            return

    # creating_kwargs = utils.parse_config_dicts(**config_kwargs)
    return _createnew(**config_kwargs)


def _createnew(INPUT_CONFIG, CROSS_VALID_CONFIG, LABEL_VALID_CONFIG,
               DATA_VALID_CONFIG, LABEL_ACTOR_CONFIG, DATA_ACTOR_CONFIG):
    """ Better creation of stuffs
    """
    try:
        data_type = INPUT_CONFIG["type"]
        data_tag =  INPUT_CONFIG["tag"]
    except KeyError as e:
        raise libex.InitialisationError(
            f"Invalid Input initialisation: {e}"
        )

    try:
        lbl_valid = validators.configure_validator(LABEL_VALID_CONFIG)
        data_valid = validators.configure_validator(DATA_VALID_CONFIG)
        cross_valid = validators.configure_xvalidator(CROSS_VALID_CONFIG)
    except TypeError as e:
        raise libex.InitialisationError(
            f"Invalid Validator initialisation: {e}"
        )

    try:
        lbl_actor = actors.configure_actor(LABEL_ACTOR_CONFIG)
        data_actor = actors.configure_actor(DATA_ACTOR_CONFIG)
    except TypeError as e:
        raise libex.InitialisationError(
            f"Invalid Actor initialisation: {e}"
        )

    return factory.create_librarian(
        datatype=data_type, datatag=data_tag,
        label_validator=lbl_valid, label_actor=lbl_actor,
        data_validator=data_valid, data_actor=data_actor,
        cross_validator=cross_valid
    )


# def _create(DATA_TYPE, DATA_TAG, CROSS_VALID_TYPE, CROSS_VALID_ARGS,
#     LABEL_VALID_TYPE, LABEL_VALID_ARGS, DATA_VALID_TYPE, DATA_VALID_ARGS,
#     LABEL_ACTOR_TYPE, LABEL_ACTOR_ARGS, DATA_ACTOR_TYPE, DATA_ACTOR_ARGS):
#     """ Create a Librarian service instance with config tags

#     Initialises the validators and actors, passes them to factory

#     Args:
#         DATA_TYPE (str): Type of data expected to be received
#         DATA_TAG  (str): Tag under which the data is found in received data
#         CROSS_VALID_TYPE  (str): Type of cross validator to use
#         CROSS_VALID_ARGS (list): Arguments to pass to cross validator init
#         LABEL_VALID_TYPE  (str): Type of label validator to use
#         LABEL_VALID_ARGS (list): Arguments to pass to label validator init
#         DATA_VALID_TYPE   (str): Type of data validator to use
#         DATA_VALID_ARGS  (list): Arguments to pass to data validator init
#         LABEL_ACTOR_TYPE  (str): Type of label actor to use
#         LABEL_ACTOR_ARGS (list): Arguments to pass to label actor init
#         DATA_ACTOR_TYPE   (str):  Type of data actor to use
#         DATA_ACTOR_ARGS  (list): Arguments to pass to data actor init

#     Returns (flask.app):
#         An app ready to run.

#     Raises:
#         InitialisationError: if initialisation fails.
#     """

#     # Setup validators and actors:
#     try:
#         lbl_valid = validators[LABEL_VALID_TYPE](*LABEL_VALID_ARGS)
#         data_valid = validators[DATA_VALID_TYPE](*DATA_VALID_ARGS)
#         cross_valid = xvalidators[CROSS_VALID_TYPE](*CROSS_VALID_ARGS)
#     except TypeError as e:
#         raise libex.InitialisationError(
#             f"Invalid Validator initialisation: {e}"
#         )

#     try:
#         lbl_actor = actors[LABEL_ACTOR_TYPE](*LABEL_ACTOR_ARGS)
#         data_actor = actors[DATA_ACTOR_TYPE](*DATA_ACTOR_ARGS)
#     except TypeError as e:
#         raise libex.InitialisationError(
#             f"Invalid Actor initialisation: {e}"
#         )


#     return factory.create_librarian(
#         datatype=DATA_TYPE, datatag=DATA_TAG,
#         label_validator=lbl_valid, label_actor=lbl_actor,
#         data_validator=data_valid, data_actor=data_actor,
#         cross_validator=cross_valid
#     )


def _fail_config(message):
    print("Failed to load Librarian configurations:")
    print("\t"+message)
    print("Exiting ...")


if __name__ == "__main__":
    fire.Fire({
        'describe': describe,
        'launch': launch,
        'create': create,
    })
