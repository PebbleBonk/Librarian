class EnvironmentVariableLoadException(Exception):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)


class InitialisationError(Exception):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)