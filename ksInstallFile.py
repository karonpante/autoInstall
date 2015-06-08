__author__ = 'karon'
# This file uses the 'templates/ksInstall'-template to autoconfigure this file

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class KsInstallFile(TextFile):
    def __init__(self, location='/tmp/', filename='ksInstall', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, root_element):
        # Get XML elements
        xml_root = root_element
        xml_time = xml_root.find('time')
        xml_users = xml_root.find('users')
        xml_services = xml_root.find('services')
        xml_packages = xml_root.find('packages')
        xml_storage = xml_root.find('storage')

        # Get configured values out of element file (XML)
        ks_install_settings = {}
        ks_install_settings.update(KsInstallFile._get_timezone_configuration(xml_time))
        ks_install_settings.update(KsInstallFile._get_users_configuration(xml_users))
        ks_install_settings.update(KsInstallFile._get_services_configuration(xml_services))
        ks_install_settings.update(KsInstallFile._get_x_configuration(xml_packages))
        ks_install_settings.update(KsInstallFile._get_storage_configuration(xml_storage))

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/ksInstall'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**ks_install_settings)

    def set_real_content(self):
        print "real"

    @staticmethod
    def _get_timezone_configuration(time_element):
        # Get configured values out of element file (XML)
        timezone = time_element.find('timezone')

        # Set values of template file
        timezone_configuration = 'timezone --isUtc {0}'.format(timezone.text)

        # Return the timezone configuration
        return {'timezone': timezone_configuration}

    @staticmethod
    def _get_users_configuration(users_element):
        # Get configured values out of element file (XML)
        root_password = users_element.find('rootpassword')
        users = []
        for user in users_element.findall('user'):
            users.append((user.text, user.get('password')))

        # Set values for template file
        rootpassword_configuration = 'rootpw --iscrypted {0}'.format(root_password.text)
        users_configuration = ''
        for user in users:
            users_configuration += 'user --name={0} --password={1} --iscrypted\n'.format(user[0], user[1])

        # Return the timezone configuration
        return {'rootpassword': rootpassword_configuration, 'users': users_configuration}

    @staticmethod
    def _get_services_configuration(services_element):
        # Get configured values out of element file (XML)
        firewall = services_element.find('firewall')
        selinux = services_element.find('selinux')
        services = []
        for service in services_element.findall('service'):
            services.append((service.text, service.get('state')))

        # Set values for template file
        firewall_configuration = 'firewall --{0}'.format(firewall.text)
        selinux_configuration = 'selinux --{0}'.format(selinux.text)

        disabled_services = []
        enabled_services = []
        for service in services:
            if service[1] == 'disabled':
                disabled_services.append(service[0])
            elif service[1] == 'enabled':
                enabled_services.append(service[0])
        services_configuration = 'services --disabled {0} --enabled {1}'.format(','.join(disabled_services), ','.join(enabled_services))

        # Return the timezone configuration
        return {'services': services_configuration, 'firewall': firewall_configuration, 'selinux': selinux_configuration}

    @staticmethod
    def _get_x_configuration(packages_element):
        # Get configured values out of element file (XML)
        x = packages_element.find('X')

        # Set values for template file
        if x.text == 'no':
            x_configuration = 'skipx'
        else:
            x_configuration = ''

        # Return the timezone configuration
        return {'X': x_configuration}

    @staticmethod
    def _get_storage_attributes_string(volume):
        general_attributes = []

        # Check what type of volume is given
        if 'type' in volume[1]:
            if volume[1]['type'] == 'partition':
                general_attributes.append('--asprimary')
            elif volume[1]['type'] == 'logical':
                volume_name = volume[0].replace('/', '')
                if volume_name == '':
                    general_attributes.append('--vgname=vglocal --name=root')
                elif volume_name == 'root':
                    general_attributes.append('--vgname=vglocal --name=rootuser')
                else:
                    general_attributes.append('--vgname=vglocal --name={0}'.format(volume_name))
            else:
                print 'type'
                exit()
        else:
            print 'type'
            exit()

        # Check what the size has to be
        if 'size' in volume[1]:
            # Check if the size is automatically generated
            if volume[1]['size'] == 'recommended' or volume[1]['size'] == 'grow':
                general_attributes.append('--{0}'.format(volume[1]['size']))
                # Check if a maximum size for this is given
                if 'maxsize' in volume[1]:
                    general_attributes.append('--maxsize={0}'.format(volume[1]['maxsize']))
            else:
                general_attributes.append('--size={0}'.format(volume[1]['size']))
        else:
            print 'size'
            exit()

        # Check which filesystem this volume must contain
        if 'fs' in volume[1]:
            general_attributes.append('--fstype={0}'.format(volume[1]['fs']))
        else:
            print 'fs'
            exit()

        # Check if there are options defined for the filesystem
        if 'fsoptions' in volume[1]:
            general_attributes.append('--fsoptions={0}'.format(volume[1]['fsoptions']))

        return ' '.join(general_attributes)

    @staticmethod
    def _get_storage_configuration(storage_element):
        partitions = []
        logical_volumes = []
        for volume in storage_element.findall('volume'):
            # Get all attributes for this volume
            attributes = volume.attrib

            # Add volume in correct array and remove the type attribute
            if attributes['type'] == 'partition':
                partitions.append((volume.text, attributes))
            elif attributes['type'] == 'logical':
                logical_volumes.append((volume.text, attributes))

        partitions_configuration = []
        for volume in partitions:
            partitions_configuration.append('part {0} {1}'.format(volume[0], KsInstallFile._get_storage_attributes_string(volume)))

        # Check if logical volumes are defined and create a physical volume/LVM partition
        if len(logical_volumes) != 0:
            # Calculate minumum size needed
            logical_volumes_size = 0
            for lvolume in logical_volumes:
                # Count all known fixed sizes
                if 'size' in lvolume[1] and lvolume[1]['size'].isdigit():
                    logical_volumes_size += int(lvolume[1]['size'])

                # If the size of a volume is variable we can use the maximum possible size, if provided...
                if 'maxsize' in lvolume[1] and lvolume[1]['maxsize'].isdigit():
                    logical_volumes_size += int(lvolume[1]['maxsize'])

            partitions_configuration.append('part pv.01 --size={0} --grow'.format(logical_volumes_size))

        logical_volumes_configuration = []
        if len(logical_volumes) != 0:
            logical_volumes_configuration.append('volgroup vglocal pv.01')
            for volume in logical_volumes:
                logical_volumes_configuration.append('logvol {0} {1}'.format(volume[0], KsInstallFile._get_storage_attributes_string(volume)))

        return {'partitions': '\n'.join(partitions_configuration), 'logvols': '\n'.join(logical_volumes_configuration)}