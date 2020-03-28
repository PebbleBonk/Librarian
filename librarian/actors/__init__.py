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