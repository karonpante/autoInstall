__author__ = 'karon'

from xml.etree import ElementTree
from urllib2 import urlopen, URLError
import networkSettings
import timeSettings
import os
from fileHandler import FileHandler

# Import Template configuration files
from keyboardFile import KeyboardFile
from i18nFile import I18nFile
from networkFile import NetworkFile
from ntpFile import NtpFile
from resolvFile import ResolvFile
from ifcfgFile import IfcfgFile
from sshdFile import SshdFile
from bondingFile import BondingFile
from hostnameFile import HostnameFile

# Directory where this script is executed
exec_path = os.path.dirname(__file__)

# DNS name for the install server
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

# Get XML information in Element files
xml_tree = ElementTree.parse(urlopen(xml_url))
xml_root = xml_tree.getroot()
xml_general = xml_root.find('general')
xml_network = xml_root.find('network')
xml_interfaces = xml_network.find('interfaces')
xml_dns = xml_network.find('dns')
xml_language = xml_root.find('language')
xml_time = xml_root.find('time')
xml_ntp = xml_time.find('ntp')

# Set general filehandler
fh = FileHandler()

# Create resolv file
resolv_file = ResolvFile(location='/tmp/')
resolv_file.set_xml_content(xml_dns)
fh.write_file(resolv_file)

# Create interface files
for xml_interface in xml_interfaces:
    if xml_interface.tag == 'interface':
        # Create interface file
        interface_systemname = networkSettings.interface_systemname(xml_interface)
        interface_file = IfcfgFile(location='/tmp/', filename='ifcfg-{0}'.format(interface_systemname))
        interface_file.set_xml_content(xml_interface)
        fh.write_file(interface_file)
    elif xml_interface.tag == 'bond':
        # Create interface file and bonding driver mapping file
        interface_file = IfcfgFile(location='/tmp/', filename='ifcfg-{0}'.format(xml_interface.get('name')))
        interface_file.set_xml_content(xml_interface)
        fh.write_file(interface_file)

# Create bonding mapping file
bonding_file = BondingFile(location='/tmp/')
bonding_file.set_xml_content(xml_interfaces)
fh.write_file(bonding_file)

# Check in which file to write the hostname
if xml_general.find('os').text.startswith('oel6') or \
        xml_general.find('os').text.startswith('rh6') or \
        xml_general.find('os').text.startswith('centos6'):
    # Create network file
    network_file = NetworkFile(location='/tmp/')
    network_file.set_xml_content(xml_general)
    fh.write_file(network_file)
elif xml_general.find('os').text.startswith('oel7') or \
        xml_general.find('os').text.startswith('rh7') or \
        xml_general.find('os').text.startswith('centos7'):
    # Create hostname file
    hostname_file = HostnameFile(location='/tmp/')
    hostname_file.set_xml_content(xml_general)
    fh.write_file(hostname_file)

# Change settings in ssh file
sshd_file = SshdFile(location='/tmp/')
sshd_file.set_real_content()
sshd_file.set_permit_root_login(xml_general)
fh.write_file(sshd_file)

# Create keyboard file
keyboard_file = KeyboardFile(location='/tmp/')
keyboard_file.set_xml_content(xml_language)
fh.write_file(keyboard_file)

# Create language file
language_file = I18nFile(location='/tmp/')
language_file.set_xml_content(xml_language)
fh.write_file(language_file)

# Create ntp file
ntp_file = NtpFile(location='/tmp/')
ntp_file.set_xml_content(xml_ntp)
fh.write_file(ntp_file)

# Set local time correct immediately
timeSettings.set_localtime(xml_ntp)