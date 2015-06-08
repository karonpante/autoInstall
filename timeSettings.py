__author__ = 'karon'

import os
from subprocess import call

exec_path = os.path.dirname(__file__)


def set_localtime(ntp_element):
    call(['ntpdate', ntp_element[0].text])
    call(['hwclock', '-wu'])