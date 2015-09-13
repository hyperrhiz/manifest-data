#!/usr/bin/python

## Author:  Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-NC-SA 4.0
##          http://creativecommons.org/licenses/by-nc-sa/4.0/


import os
import urllib2
import subprocess
import socket
import getpass
import platform
import glob
import re


class StatusCodeError(Exception):
    pass


class TCPFlowError(Exception):
    pass


class IPV6Error(Exception):
    pass

###########################################################
#   Checks
###########################################################

#   For fixing file permissions because script is run as
#   root
try:
    with open(os.path.join(os.path.dirname(__file__), '.ids'), 'rb') as ids:
        UID, GID = ids.read().split()
except (IOError, OSError):
    raise Exception('Please run setup.sh first.')

OUTPUT = os.path.join(os.path.dirname(__file__), 'tcpflow')
PLATFORM = platform.system()

if PLATFORM == "Windows":
    raise Exception("You can't run this on Windows... Sorry!")

if not getpass.getuser() == 'root':
    raise Exception('Please run this script as root. i.e. sudo python ...')


###########################################################
#   For fixing IP Addresses
###########################################################


def pad_ip_address(s):
    """
    add zero padding for ip address
    :param s: string ip address
    """

    s = [int(i) for i in s.split('.')]
    return '{:03d}.{:03d}.{:03d}.{:03d}'.format(*s)


def get_external_ip():
    """
    pings external website to get external ip address
    to replace internal ip address in file output
    """

    urls = ['http://ifconfig.co', 'http://ifconfig.me']
    headers = {'User-Agent': 'curl/'}
    for url in urls:
        request = urllib2.Request(url, headers=headers)
        try:
            r = urllib2.urlopen(request)
            if r.code != 200:
                raise StatusCodeError
        except (urllib2.URLError, StatusCodeError) as e:
            print('There was an error connecting to {}... trying something else.'.format(url))
        else:
            ip = r.read().strip()
            print("Your external IP address is {}".format(ip))
            try:
                return pad_ip_address(ip)
            except ValueError:
                if ":" in ip:
                    print('\033[91m\nIt looks like you are connecting from an IPv6 address. Google maps functionality will '
                          'unfortunately be broken for the data collected during this session.\n\nRestarting this script '
                          'might resolve the problem.\n\033[0m')
            return None
    else:
        raise e


def get_internal_ip():
    """
    read local ip address
    """
    if PLATFORM == 'Darwin':
        ip = socket.gethostbyname(socket.gethostname())
    elif PLATFORM == "Linux":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        ip = s.getsockname()[0]
    if ip.startswith('127.0'):
        raise Exception('Please make sure you are connected to the internet.')
    print('Your internal IP address is {}'.format(ip))
    return pad_ip_address(ip)


def fix_filenames(i, e, d):
    """
    replace internal ip with external
    :param i: internal ip
    :param e: external ip
    :param d: directory
    """
    d += '/*'
    files = glob.glob(d)
    for f in files:
        if i in f:
            new = f.replace(i, e)
            os.rename(f, new)

###########################################################


def main():

    print("outputting files to {}".format(OUTPUT))

    #   Try to make output directory. Pass if it already
    #   exists.
    try:
        os.mkdir(OUTPUT)
    except OSError:
        pass

    #   Retrieve internal and external IP addresses to
    #   allow replacement when program is terminated.
    #
    #   If external_ip is IPv6, return will be None.
    external_ip = get_external_ip()
    internal_ip = get_internal_ip()

    print("starting tcpflow... you are being watched.\n")
    print('press ctrl-c to exit\n')

    #   Determine correct location for tcpflow. Different
    #   for Darwin vs Linux.
    paths = ['/usr/local/bin/tcpflow', '/usr/bin/tcpflow']
    try:
        tcpflow = [p for p in paths if os.path.isfile(p)][0]
    except IndexError:
        raise TCPFlowError('Please make sure TCPFlow is installed correctly. '
                           'Run the setup file, if you haven\'t already.')

    #   This starts tcpflow and runs it until ctrl-c is
    #   pressed.
    interfaces = ["en1", "eth0", "eth1", "eth2", "wlan0", "wlan1", "en0", "wifi0",
                  "ath0", "ath1", "ppp0"]

    if PLATFORM == "Darwin":
        proc = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        istr = "|".join(interfaces)
        adapters = re.findall(r'({}).*?status: (.*?)\n'.format(istr), out, flags=re.S)
        interfaces = [x[0] for x in adapters if x[1] == "active"]

    try:
        for iface in interfaces:
            _args = [tcpflow, '-a', '-Ft', '-o', OUTPUT, '-i', iface]
            proc = subprocess.Popen(_args, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if err:
                #   No device means wrong adapter.
                #   Therefore we ignore that error.
                if "No such device exists" not in err:
                    raise TCPFlowError(err)
    except KeyboardInterrupt:
        #   Fixes filenames to replace internal with
        #   external IP addresses.
        print('Cleaning up...')

        #   If external_ip is IPv6 (ie None), don't replace it
        if external_ip:
            fix_filenames(internal_ip, external_ip, OUTPUT)

        #   Need to fix file permissions because tcpflow
        #   requires running as root and therefore creates
        #   output files as root.
        print('Fixing file permissions...')
        subprocess.call('chown -R {0}:{1} {2}'.format(UID, GID, OUTPUT), shell=True)
        print('all done!')
    else:
        #   This means all adapters have been tried and none
        #   found working.
        raise TCPFlowError("TCPFlow couldn't find a working adapter. "
                           "Is your networking card active?")

if __name__ == '__main__':
    main()
