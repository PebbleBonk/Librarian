class InitialisationError(Exception):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)


class ValidationError(Exception):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)


class ConfigurationError(Exception):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)