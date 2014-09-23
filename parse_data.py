#!/usr/bin/python

## Author: 	Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-SA 3.0
##			http://creativecommons.org/licenses/by-sa/3.0/

## The IP geolocation data is provided by 
## http://www.ip2location.com

"""
run using:
python (path_to)/parse_ip.py

replace (path_to) with the full path
---------------
creates an .xyz 3d-model @  ~/Desktop/tcpflow_parse.xyz
from IP address data
or
creates an .html google map of data connections
"""
from __future__ import print_function
import os
import glob
import re
import random
from argparse import ArgumentParser
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATE = datetime.now().strftime('%m-%d-%Y')

parser = ArgumentParser()
parser.add_argument('-g', '--geolocate', dest="geo", action="store_true", 
						default=False, help="geolocates ip addresses")
parser.add_argument('-i', '--input', dest="input", action="store",
					default=os.path.join(BASE_DIR, 'tcpflow'), 
					help="Sets input folder for TCPflow files.")
parser.add_argument('-o', '--output', dest="output", action="store",
					default=os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz'),
					help="""Sets output file for results. Can be either full
					path or path relative to tcpflow directory""")
parser.add_argument('-v', '--verbose', dest='debug', action="store_true",
					default=False, help="Displays more information to console.")
args = parser.parse_args()

#	Handle relative paths
if not args.output.startswith(('/', '~/')):
	args.output = os.path.join(BASE_DIR, args.output)
if not args.input.startswith(('/', '~/')):
	args.input = os.path.join(BASE_DIR, args.input)

#	Handle unexpected filenames
if args.geo and not args.output.endswith('.html'):
	if args.output == os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz'):
		default = True
	else:
		default = False
	args.output = os.path.join(BASE_DIR, 'tcpflowmap-' + DATE + '.html')
	if not default:
		print("Output path seems incorrect... setting output to {0}".format(args.output))
elif not args.geo and not args.output.endswith('.xyz'):
	args.output = os.path.join(BASE_DIR, 'tcpflow-' + DATE + '.xyz')
	print("Output path seems incorrect... setting output to {0}".format(args.output))

spl = re.compile(
				r"(?P<ts>\d+)T"
				r"(?P<orig>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<orig_port>\d+)\-"
				r"(?P<dest>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<dest_port>\d+)"
				)

def logger(*s):
	if args.debug:
		print(*s)

class XYZData:
	"""
	data wrapper for xyz data
	"""
	def __init__(self, **kwargs):
		# replace . in ip addresses so we can divide it
		d = dict((k,int(v.replace('.', ''))) for k,v in kwargs.iteritems())
		self.__dict__.update(d)

class LocData:
	"""
	data wrapper for geolocation data
	"""
	def __init__(self, **kwargs):
		self.orig = self.str_format(kwargs['orig'])
		self.dest = self.str_format(kwargs['dest'])

	def str_format(self, s):
		"""
		strips leading 0 from IP address blocks
		"""
		a = s.split('.')
		return '.'.join([z.lstrip('0') for z in a])

def split_name(f):
	"""
	splits filename according to regex defined above
	"""
	split = spl.search(f)
	if split:
		return split.groupdict()
	return None

def parse_filenames(files):
	"""
	parse timestamp, origin ip address and port, destination ip address and port;
	divide origin ip address by origin port, destination ip address by dest port;
	shuffle columns and rejoin with new lines
	"""
	
	s = []
	for f in files:
		dct = split_name(f)
		if dct:
			o = XYZData(**dct)
			q = [o.ts, o.orig/o.orig_port, o.dest/o.dest_port]
			random.shuffle(q)
			s.append((' '.join((str(n) for n in q))))
	return '\n'.join(s)

def geolocate_ips(files):
	"""
	create google map of geolocated IP addresses with paths
	connecting points
	"""
	import random
	import sys
	#	Add to python path to allow import
	sys.path.append('./libs/pygmaps-0.1.1-py2.7.egg')
	sys.path.append('./libs/')
	import IP2Location
	import pygmaps

	#	Initialize IP2Location obj
	locobj = IP2Location.IP2Location()
	loc_path = os.path.join(os.path.dirname(__file__), 
							'data/IP2LOCATION-LITE-DB11.BIN')
	try:
		locobj.open(loc_path)
	except:
		raise Exception('Could not find IP2Location binary... '
						'Make sure it is in {0}/data'.format(BASE_DIR))
	s = []
	mymap = pygmaps.maps(37.428, -122.145, 4)
	for f in files:
		dct = split_name(f)
		if dct:
			d = LocData(**dct)
			orig_latlong = geolocate(locobj, d.orig)
			dest_latlong = geolocate(locobj, d.dest)
			out = [orig_latlong, dest_latlong]
			if out not in s:
				s.append(out)
	for path in s:		
		if (0.0, 0.0) not in path:
			#	sets random hex color for gmaps path
			r = lambda: random.randint(0, 255)
			h = '#%02X%02X%02X' % (r(),r(),r()) 
			logger("adding path for {0}".format(path))
			mymap.addpath(path, h)
	mymap.draw(args.output)

	#	for attribution of IP data
	with open(args.output, 'ab') as fi:
		fi.write("""
			<html>
				<body>
					<p style="text-align: center">The IP geolocation data is 
					provided by <a href="http://www.ip2location.com">
					http://www.ip2location.com</a></p>
				</body>
			</html>""")
	return None

def geolocate(locobj, ip):
	try:
		req = locobj.get_all(ip)
	except:
		return (0.0, 0.0)
	return (req.latitude, req.longitude)

def main():
	files = glob.glob(args.input + '/*')
	logger(files)
	if not files:
		raise Exception("No files to look at. Run tcpflow before parsing.")
	files = [os.path.basename(f) for f in files]
	if args.geo:
		output = geolocate_ips(files)
	else:
		output = parse_filenames(files)
	
	if output:
		logger(output)

	if not args.geo:
		with open(args.output, 'wb') as f:
			f.write(output)
	print('Success! You can find your files at {}'.format(args.output))

if __name__=="__main__":
	main()
