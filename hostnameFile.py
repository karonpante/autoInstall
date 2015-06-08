__author__ = 'karon'
# This file uses the 'templates/hostname'-template to autoconfigure this file

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class HostnameFile(TextFile):

    def __init__(self, location='/etc/', filename='hostname', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, general_element):
        # Get configured values out of element file (XML)
        hostname = general_element.find('hostname')

        # Set values of template file
        hostname_configuration = hostname.text

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/hostname'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'hostname': hostname_configuration})

    def set_real_content(self):
        print "real"
