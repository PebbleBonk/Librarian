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
        setup = self.__class__.__name__ +" with setup:"
        for var, val in vars(self).items():
            setup += f"\n\t{var}: {val}"
        return setup

    def __repr__(self):
        return str(self).replace('\n', ', ').replace('\t', '').strip()

    @classmethod
    def describe(cls):
        return ''.join([cls.__name__, '\n', cls.__doc__.strip('\n')])


class CompositeActor:
    """ Compose a combination of several actors

        Checks the object agains every actors

        Args:
            *validators: actors to compose the actor from
    """
    def __init__(self, *actors):
        self.actors = list(actors) if actors is not None else []

    def  __add__(self, other):
        self.actors.append(other)
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __call__(self, obj):
        return [actor.act(obj) for actor in self.actors]

    def __str__(self):
        string = self.__class__.__name__ +" with Actors:"
        for actor in self.actors:
            string += "\n\t"+str(actor).replace('\n', '\n\t')
        return string

    def __repr__(self):
        return str(self).replace('\n', ', ').replace('\t', '').strip()
