__author__ = 'karon'

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class SshdFile(TextFile):
    def __init__(self, location='/etc/ssh/', filename='sshd_config', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, language_element):
        print 'xml'

    def set_real_content(self):
        fh = FileHandler(location=self.location)
        self.content = fh.read_file(self)

    def set_permit_root_login(self, general_element):
        # Get configured values out of element file (XML)
        ssh_rootlogin = general_element.find('rootsshlogin')

        ssh_config = ''
        for line in self.content.split('\n'):
            # Find configurable variable, make sure it is the variable setting and not something in comment.
            if 'PermitRootLogin' in line and len(line) < 25:
                if ssh_rootlogin.text == 'no':
                    ssh_config += 'PermitRootLogin no\n'
                elif ssh_rootlogin.text == 'yes':
                    ssh_config += 'PermitRootLogin yes\n'
            else:
                ssh_config += '{0}\n'.format(line)

        self.content = ssh_config