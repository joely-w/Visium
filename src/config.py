import os

from src.definitions import *


class Config(object):
    def __init__(self):
        try:
            uploads = os.environ['UPLOAD_DIR']
            self.UPLOAD_FOLDER = os.path.join(uploads)
        except KeyError:
            self.UPLOAD_FOLDER = os.path.join(ROOT_DIR, '../uploads/')

        # If upload directory doesn't exist then create it
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
