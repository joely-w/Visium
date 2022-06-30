import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    UPLOAD_FOLDER = os.path.join(basedir, '../uploads/')

    ALLOWED_UPLOAD_EXTENSIONS = {'zip'}

    def __init__(self):
        # If upload directory doesn't exist then create it
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
