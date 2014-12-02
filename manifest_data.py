#!/usr/bin/python

## Author: 	Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-SA 3.0
##			http://creativecommons.org/licenses/by-sa/3.0/

from argparse import ArgumentParser
import os
import urllib2
import subprocess
import socket
import getpass
import platform
import glob

parser = ArgumentParser()
parser.add_argument('-o', '--output', dest="output", action="store",
					default=os.path.join(os.path.dirname(__file__), 'tcpflow'), 
					help="Sets output folder for TCPflow files.")
parser.add_argument('-i', '--interface', dest="iface", action="store",
					default="en1", help="Sets networking interface adapter.")
args = parser.parse_args()

###########################################################
#	Checks
###########################################################
if platform.system() == "Windows":
	raise Exception("You can't run this on Windows... Sorry!")

if not getpass.getuser() == 'root':
	raise Exception('Please run this script as root. i.e. sudo python ...')

#	For fixing file permissions because script is run as
#	root
try:
	with open(os.path.join(os.path.dirname(__file__), '.ids'), 'rb') as ids:
		UID, GID = ids.read().split()
except IOError, OSError:
	raise Exception('Please run setup.sh first.')

###########################################################
#	For fixing IP Addresses
###########################################################

def pad_ip_address(s):
	"""
	add zero padding for ip address
	"""
	s = [int(i) for i in s.split('.')]
	return '{:03d}.{:03d}.{:03d}.{:03d}'.format(*s)

def get_external_ip():
	"""
	pings external website to get external ip address
	to replace internal ip address in file output
	"""
	url = 'http://ifconfig.me'
	headers = {'User-Agent': 'curl/'}
	request = urllib2.Request(url, headers=headers)
	r = urllib2.urlopen(request)
	if r.code != 200:
		raise Exception('There was an error... please make sure you are'
						'connected to the internet.')
	return pad_ip_address(r.read().strip())

def get_internal_ip():
	"""
	read localhost ip
	"""
	ip = socket.gethostbyname(socket.gethostname())
	if ip == '127.0.0.1':
		raise Exception('Please make sure you are connected to the internet.')
	return pad_ip_address(ip)

def fix_filenames(i, e, d):
	d += '/*'
	files = glob.glob(d)
	print(files)
	for f in files:
		if i in f:
			new = f.replace(i, e)
			os.rename(f, new)

###########################################################

def main():
	print("outputting files to {}".format(args.output))
	try:
		os.makedir(args.output)
	except:
		pass
	external_ip = get_external_ip()
	internal_ip = get_internal_ip()
	print("starting tcpflow... you are being watched.")
	print('press ctrl-c to exit\n')
	try:
		subprocess.call('/usr/local/bin/tcpflow -a -Ft -o {0} -i {1}'.format(args.output, args.iface), shell=True)
	except KeyboardInterrupt:
		print('Cleaning up...')
		fix_filenames(internal_ip, external_ip, args.output)

		#	Need to fix file permissions because tcpflow 
		#	requires running as root and therefore creates
		#	output files as root
		print('Fixing file permissions...')
		subprocess.call('chown -R {0}:{1} {2}'.format(UID, GID, args.output), shell=True)
		print('all done!')

if __name__ == '__main__':
	main()