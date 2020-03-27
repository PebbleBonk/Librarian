from librarian.validators import validator
from librarian.validators import crossvalidators
from librarian.validators import filevalidator
from librarian.validators import typevalidator
from librarian.validators import keyvalidator
from librarian.validators import imagevalidator



validators = {
    'file': filevalidator.FileValidator,
    'type': typevalidator.TypeValidator,
    'key':  keyvalidator.KeyValidator,
    'img': imagevalidator.ImageValidator,
    'none': validator.DummyValidator
}

xvalidators = {
    'none': crossvalidators.DummyCrossValidator,
    'fname': crossvalidators.MacthFileNames
}