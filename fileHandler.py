__author__ = 'karon'

class FileHandler(object):
    def __init__(self, location=''):
        self.location = location

    def read_content(self):
        with open(self.location, 'r') as read_file:
            # Get file content as string
            return read_file.read()

    def read_file(self, text_file):
        with open(text_file.location+text_file.filename, 'r') as read_file:
            return read_file.read()

    def write_content(self, content):
        with open(self.location, 'w') as write_file:
            write_file.write(content)

    def write_file(self, text_file):
        with open(text_file.location+text_file.filename, 'w') as write_file:
            write_file.write(text_file.content)

    @staticmethod
    def remove_file():
        print 'removed'

    @staticmethod
    def get_owner():
        print 'owners'

    @staticmethod
    def get_permissions(self):
        print 'permissions'
