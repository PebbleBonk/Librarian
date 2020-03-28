from librarian.validators.validator import Validator
from librarian.validators.exceptions import ValidationError, InitialisationError
from PIL import Image

class ImageValidator(Validator):
    """ Validator for checking if file is a valid image

        Checks for load, pillow verify and height and width
        NOTE: Use h, w = 0,0 to skip dimension check

        Args:
            h (int): height of the image
            w (int): width of the image

        Returns (bool):
            Whether the validation was successful
    """
    def __init__(self, h: int, w: int):
        super().__init__()
        self.h = int(h)
        self.w = int(w)

    def __call__(self, obj):
        try:
            im = Image.open(obj)
        except Exception as e:
            raise ValidationError("Could not open the image: "+str(e))

        if (self.h and im.height != self.h) or (self.w and im.width != self.w):
            print("1", (self.h and im.height != self.h))
            print("2", (self.w and im.width != self.w))
            raise ValidationError("Image dimensions do not match")

        try:
            im.verify()
        except Exception as e:
            raise ValidationError("Could not verify the image: "+str(e))

