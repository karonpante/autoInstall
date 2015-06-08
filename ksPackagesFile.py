__author__ = 'karon'
# This file uses the 'templates/ksPackages'-template to autoconfigure this file


from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class KsPackagesFile(TextFile):
    def __init__(self, location='/tmp/', filename='ksPackages', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, packages_element):
        # Get configured values out of element file (XML)
        packages = []
        for package in packages_element.findall('package'):
            packages.append(package.text)

        # Set values of template file
        packages_configuration = ''
        for package in packages:
            packages_configuration += '{0}\n'.format(package)

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/ksPackages'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'packages': packages_configuration})

    def set_real_content(self):
        print "real"
