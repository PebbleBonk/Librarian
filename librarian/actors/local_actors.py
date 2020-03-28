from librarian.actors.actor import Actor
import json
from PIL import Image
import os


class PrinterActor(Actor):
    """ Prints information about the data. Great for debugging!

        Can be configured to print more info with *args
    """
    def __init__(self, *args):
        super().__init__()
        self.description = "Prints the given data"
        self.extras = args

    def act(self, data, uid):
        """ Saves the data into the supplied directory """
        print("[PRINTER]:", self.extras, data)
        return f"\tDATA: {data}\n\tUID: {uid}\n\t{self.extras}"



class FileActor(Actor):
    """ Saves the given data objects as a file

        Args:
            directory (str): Directory to which the files are saved. Will
                be created if doesn't exist

        NOTE: data is expected to be a FileStorage object
    """
    def __init__(self, directory):
        super().__init__()
        self.description = "Saves object to a local file"
        self.directory = directory
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def act(self, data, uid):
        """ Saves the data into the supplied directory """
        #with open(os.path.join(self.directory, data.filename), 'w') as f:
        #    f.write(data)
        data.save(os.path.join(self.directory, data.filename))
        return "File saved succesfully"


class ImageActor(Actor):
    """ Saves object to a local image file

        Args:
            directory (str): Directory to which the files are saved. Will
                be created if doesn't exist
    """
    def __init__(self, directory):
        super().__init__()
        self.description = "Saves object ot a local image file"
        self.directory = directory
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def act(self, data, uid):
        im = Image.open(data)
        im.save(os.path.join(self.directory, uid+'.jpg'))


class JsonActor(Actor):
    """ Saves object ot a local json file

        Args:
            jsonfile (str): json file to which save the data. If a path,
                the directory should already exist!
    """
    def __init__(self, jsonfile):
        super().__init__()
        self.description = "Saves object ot a local json file"
        self.jsonfile = jsonfile

    def act(self, data, uid):
        """ Saves the data to specified json file by appending """
        # Save as a list of objects:
        data["uid"] = uid
        data = [data]
        if os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'r') as f:
                data += json.load(f)


        with open(self.jsonfile, 'w') as f:
            json.dump(data, f)
        return "Json saved successfully"


class DummyActor(Actor):
    """ A dummy actor: does nothing, i.e. passes everything.

    Great for debugging. Takes no arguments.
    """
    def __init__(self):
        super().__init__()
        self.description = "Does nothing"

    def act(self, data, uid):
        return "Did nothing"
