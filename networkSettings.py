__author__ = 'karon'

from binascii import unhexlify, hexlify
import os

exec_path = os.path.dirname(__file__)


def get_interface_addresses():
    # Get list of interface names and there mac addresses on the system
    #system_interface_names = {}
    interface_addresses = {}
    for interface in os.listdir('/sys/class/net'):
        with open('/sys/class/net/{0}/address'.format(interface)) as interface_file:
            #system_interface_names[interface_file.read()[:17].lower()] = interface.lower()
            interface_addresses[interface] = interface_file.read()[:17].lower().replace(':', '')
    return interface_addresses


def get_interface_systemname(mac_address):
    # Get list of interface names and accompanied mac addresses on system
    #system_interface_names = {}
    for interface in os.listdir('/sys/class/net'):
        with open('/sys/class/net/{0}/address'.format(interface)) as interface_file:
            #system_interface_names[interface_file.read()[:17].lower()] = interface.lower()
            if interface_file.read()[:17].lower() == mac_address.lower():
                return interface
    return None


def interface_systemname(interface_element):
    mac = interface_element.find('mac')             # Get mac address of interface

    for interface in os.listdir('/sys/class/net'):
        with open('/sys/class/net/{0}/address'.format(interface)) as interface_file:
            #system_interface_names[interface_file.read()[:17].lower()] = interface.lower()
            if interface_file.read()[:17].lower() == form_mac(mac).lower():
                return interface
    return None


def form_mac(mac_address):
    return ':'.join(hexlify(x) for x in unhexlify(mac_address.text)).lower()


