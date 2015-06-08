__author__ = 'karon'
# This file uses the 'templates/ifcfg'-template to autoconfigure this file
# Values for this template are taken by the language element that looks like: ...

from textFile import TextFile
from fileHandler import FileHandler
from os import path
import networkSettings

# Directory where this file is located
exec_path = path.dirname(__file__)


class IfcfgFile(TextFile):
    def __init__(self, location='/etc/sysconfig/network-scripts/', filename='ifcfg-None', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, interface_element):
        # Get configured values out of element file (XML)
        name = interface_element                        # Get name of interface
        mac = interface_element.find('mac')             # Get mac address of interface
        ip = interface_element.find('ip')               # Get IP address of interface
        mask = interface_element.find('mask')           # Get subnet mask of interface
        gateway = interface_element.find('gateway')     # Get default gateway for server
        bond = interface_element.find('bond')         # Get the bond interface for which this interface is a member

        # Set values of template file:
        #   Create string with name configuration
        name_configuration = 'NAME={0}'.format(name.get('name'))

        # Create string with MAC address configuration
        # Decode the HEX block to 8 bit characters (binary ascii)
        # Iterate each character, change it back to hex and place:
        if mac is not None:
            mac_configuration = 'HWADDR={0}'.format(networkSettings.form_mac(mac))
        else:
            mac_configuration = ''

        # Create string with the systems device name
        if interface_element.tag == 'interface':
            interface_name_configuration = 'DEVICE={0}'.format(networkSettings.interface_systemname(interface_element))
        elif interface_element.tag == 'bond':
            interface_name_configuration = 'DEVICE={0}'.format(name.get('name'))

        # Create string with ip configuration
        if ip is not None:
            ip_configuration = 'IPADDR={0}'.format(ip.text)
        else:
            ip_configuration = ''

        # Create string with mask configuration
        if mask is not None:
            mask_configuration = 'NETMASK={0}'.format(mask.text)
        else:
            mask_configuration = ''

        # Create string with gateway configuration
        if gateway is not None:
            gateway_configuration = 'GATEWAY={0}'.format(gateway.text)
        else:
            gateway_configuration = ''

        # Create string with Bonding configuration
        if bond is not None:
            bond_configuration = 'MASTER={0}\nSLAVE=yes'.format(bond.text)
        else:
            bond_configuration = ''

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/ifcfg'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'name': name_configuration,
                                                            'mac': mac_configuration,
                                                            'ip': ip_configuration,
                                                            'mask': mask_configuration,
                                                            'device': interface_name_configuration,
                                                            'gateway': gateway_configuration,
                                                            'bond': bond_configuration})

    def set_real_content(self):
        print "real"
