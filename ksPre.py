__author__ = 'karon'

import os
from xml.etree import ElementTree
from urllib2 import urlopen, URLError
import networkSettings
from fileHandler import FileHandler

# Import Template Configuration files
from ksInstallFile import KsInstallFile
from ksPackagesFile import KsPackagesFile

# Install server DNS name
install_server = 'install'


# Check if a certain URL exists and is reachable
# Return True or False
def check_url(url):
    try:
        urlopen(url)
    except URLError:
        return False
    else:
        return True


# Find correct XML file which is based on one of the MAC addresses of the machine
xml_url = None
for interface_address in networkSettings.get_interface_addresses().values():
    if check_url('http://{0}/linux/servers/{1}.xml'.format(install_server, interface_address)):
        xml_url = 'http://{0}/linux/servers/{1}.xml'.format(install_server, interface_address)
# If no correct XML file is found, stop the script
if xml_url is None:
    exit()

# Get directory where this script is located
exec_path = os.path.dirname(__file__)

# Get XML information in Element files
xml_tree = ElementTree.parse(urlopen(xml_url))
xml_root = xml_tree.getroot()
xml_packages = xml_root.find('packages')

# Set general filehandler
fh = FileHandler()

# Create Install kickstart file
ksInstall_file = KsInstallFile()
ksInstall_file.set_xml_content(xml_root)
fh.write_file(ksInstall_file)

# Create Packages kickstart file
ksPackages_file = KsPackagesFile()
ksPackages_file.set_xml_content(xml_packages)
fh.write_file(ksPackages_file)