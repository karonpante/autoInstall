__author__ = 'karon'
# This file uses the 'templates/ntp.conf'-template to autoconfigure this file
# Values for this template are taken by the language element that looks like: ...

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class NtpFile(TextFile):

    def __init__(self, location='/etc/', filename='ntp.conf', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, ntp_element):
        # Get configured values out of element file (XML) and set values of template files.
        ntp_server_configuration = ''
        for ntp_server in ntp_element:
            ntp_server_configuration += 'server {0}\n'.format(ntp_server.text)

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/ntp.conf'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'ntp': ntp_server_configuration})

    def set_real_content(self):
        print "real"
