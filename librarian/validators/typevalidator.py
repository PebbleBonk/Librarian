from librarian.validators.validator import Validator
from librarian.validators.exceptions import ValidationError, ConfigurationError


class TypeValidator(Validator):
    """ An expandable class for validating types of variables

        arg example: {"name": "str", "age": "int" "married": "bool"}
        The types will be converted to type objects during initialisation.
        I.e. "str" becomes str, "float" becomes float etc.
        Currently supported types: (int, float, str, bool)

        Args:
            config (dict): keys to be checked and expected types as strings
                . E.g.: {"name": "str", "age": "int" "married": "bool"}

        Returns (bool):
            Whether the validation was successful
    """
    def __init__(self, config: dict):
        if not isinstance(config, dict):
            raise InitialisationError("Invalid arguments")
        super().__init__()
        # Currently supported types and their actions:
        supported_types = {
            'str': str,
            'float': float,
            'int': int,
            'bool': bool,
        }
        # Parse config json:
        self.validation_dict = {
            # Key to validate: funciton to check expected type
        }
        for k, v in config.items():
            t = supported_types.get(v, False)
            if not t:
                raise ConfigurationError(f"Supplied type not supported: {v}")
            self.validation_dict[k] = t

    def __call__(self, obj):
        for key, val in iter(self.validation_dict.items()):
            if key not in obj:
                raise ValidationError(f"Required field {key} not found")

            if not isinstance(obj[key], self.validation_dict[key]):
                raise ValidationError(
                    f"Invalid type ({type(obj[key])})" +
                    f" for {key}. Expected ({val})"
            )
        return True
