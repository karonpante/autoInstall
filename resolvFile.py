__author__ = 'karon'
# This file uses the 'templates/resolv.conf'-template to autoconfigure this file
# Values for this template are taken by the language element that looks like: ...

from textFile import TextFile
from fileHandler import FileHandler
from os import path

# Directory where this file is located
exec_path = path.dirname(__file__)


class ResolvFile(TextFile):

    def __init__(self, location='/etc/', filename='resolv.conf', content=''):
        TextFile.__init__(self, location, filename, content)

    def set_xml_content(self, dns_element):
        # Get configured values out of element file (XML)
        domain = dns_element.find("domain")  # domain elemant
        dnsservers = dns_element.findall("dnsserver")  # List of dnsserver elements
        searchdomains = dns_element.findall("searchdomain")  # List of searchdomain elements

        # Set values of template file:
        #   Create string with domain configuration
        if domain is not None:
            domain_configuration = 'domain {0}'.format(domain.text)
        else:
            domain_configuration = '#domain'

        #   Create string with searchdomains configuration
        if domain is not None:
            searchdomains_array = [domain.text]
        else:
            searchdomains_array = []
        if len(searchdomains) != 0 or len(searchdomains_array) != 0:
            for searchdomain in searchdomains:
                searchdomains_array.append(searchdomain.text)
            searchdomains_configuration = 'search {0}'.format(' '.join(searchdomains_array))
        else:
            searchdomains_configuration = '#search'

        #   Create string with dnsservers configuration
        dnsservers_configuration = ''
        for dns_server in dnsservers:
            dnsservers_configuration += 'nameserver {0}\n'.format(dns_server.text)

        # Read template file
        fh_template = FileHandler(path.join(exec_path, 'templates/resolv.conf'))

        # Merge template file and template values together and use it as new content
        self.content = fh_template.read_content().format(**{'domain': domain_configuration,
                                                            'searchdomains': searchdomains_configuration,
                                                            'dnsservers': dnsservers_configuration})

    def set_real_content(self):
        print "real"