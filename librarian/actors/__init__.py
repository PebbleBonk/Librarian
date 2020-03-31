from librarian.actors import local_actors
from librarian.actors import mongoactor
from librarian.actors import s3actor
from librarian.actors import actor

actors = {
    'S3': s3actor.S3Actor,
    'mongo': mongoactor.MongoActor,
    'file': local_actors.FileActor,
    'json': local_actors.JsonActor,
    'none': local_actors.DummyActor,
    'print': local_actors.PrinterActor,
    'image': local_actors.ImageActor,
}


def configure_actor(config):
    """ Create an actor using configuration

        All the different actors given in config are composed into
        one single Actor. The actions are done in order given.

        Args:
            config (list): List of config dicts to create the actor

        Returns (Actor):
            Actor class to act on data.

        Raises:
            KeyError if configuration key is not found in options.
    """
    # No validato used, return just a dummy:
    if len(config) == 0:
        return local_actors.DummyActor()

    # Single validator
    elif len(config) == 1:
        config = config[0]
        tag = config['actor']
        args = config.get('args',[])
        kwargs = config.get('kwargs', {})
        return actors[tag](*args, **kwargs)

    # Compose a validator using multiple validators:
    else:
        composite = actor.CompositeActor()
        for c in config:
            tag = c['actor']
            args = c.get('args',[])
            kwargs = c.get('kwargs', {})
            composite += actors[tag](*args, **kwargs)
        return composite