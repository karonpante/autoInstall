__author__ = 'karon'
# This file uses the 'templates/i18n'-template to autoconfigure this file

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class I18nFile(TextFile):

    def __init__(self, location='/etc/sysconfig/', filename='i18n', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, language_element):
        # Get configured values out of element file (XML)
        language = language_element.find('language')

        # Set values of template file
        language_configuration = 'LANG={0}'.format(language.text)

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/i18n'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'language': language_configuration})

    def set_real_content(self):
        print "real"
