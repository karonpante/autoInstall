__author__ = 'karon'
# This file uses the 'templates/bonding.conf'-template to autoconfigure this file
# Values for this template are taken by the language element that looks like: ...

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class BondingFile(TextFile):

    def __init__(self, location='/etc/modprobe.d', filename='bonding.conf', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, interfaces_element):
        # Get configured values out of element file (XML)
        bondings = []
        for interface_element in interfaces_element:
            if interface_element.tag == 'bond':
                name = interface_element.get('name')        # Name of bond interface
                miimon = interface_element.get('miimon')    # Monitoring setting for bond interface
                mode = interface_element.get('mode')        # Bonding mode for interface

                bondings.append('alias {0} bonding\noptions {0} miimon={1} mode = {2}'.format(name, miimon, mode))

        # Create string with bondings configuration
        bondings_configuration = "\n".join(bondings)

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/bonding.conf'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'bondings': bondings_configuration})

    def set_real_content(self):
        print "real"
