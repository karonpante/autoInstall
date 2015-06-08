__author__ = 'karon'
# This file uses the 'templates/keyboard'-template to autoconfigure this file
# Values for this template are taken by the language element that looks like: ...

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class KeyboardFile(TextFile):

    def __init__(self, location='/etc/sysconfig/', filename='keyboard', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, language_element):
        # Get configured values out of element file (XML)
        console_layout = language_element.find('keyboard')
        # Get X keyboard layout values
        xmap = KeyboardFile.get_keyboard_xmaps()[console_layout.text]

        # Set values of template file
        keytable_configuration = 'KEYTABLE=\"{0}\"'.format(console_layout.text)
        model_configuration = 'MODEL=\"{0}\"'.format(xmap['model'])
        layout_configuration = 'LAYOUT=\"{0}\"'.format(xmap['layout'])

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/keyboard'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'keytable': keytable_configuration,
                                                            'model': model_configuration,
                                                            'layout': layout_configuration})

    def set_real_content(self):
        print "real"

    @staticmethod
    def get_keyboard_xmaps():
        with open(path.join(exec_path,'tables/kbd-model-map')) as myfile:
            # Save file as string
            kbd_file = myfile.readlines()

            kbd_maps = {}
            for line in kbd_file:
                if not line.startswith('#'):
                    # Make all tabs spaces
                    # Get each value seperated by spaces
                    # Only give the first 3 values per line
                    kbd_map = (line.replace('\t', ' ').split()[0:3])
                    kbd_maps[kbd_map[0]] = {'layout': kbd_map[1], 'model': kbd_map[2]}
        return kbd_maps