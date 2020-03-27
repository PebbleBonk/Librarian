class Actor:
    """ Base class for Actors. Cannot work by itself

    The inheriting classes must implement the __init__ and act()
    methods. The act() method must accept arguments "data" and "uid"
    """
    def __init__(self):
        pass

    def act(self, data, uid):
        raise NotImplementedError("Inherited method not implemented")

    def __str__(self):
        setup = self.__class__.__name__ +" with setup:\n"
        for var, val in vars(self).items():
            setup += f"\t{var}: {val}\n"
        return setup

    def __repr__(self):
        return str(self).replace('\n', ' ').replace('\t', '')

    @classmethod
    def describe(cls):
        return ''.join([cls.__name__, '\n', cls.__doc__.strip('\n')])