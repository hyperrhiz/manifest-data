## Author: 	Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-NC-SA 4.0
##			http://creativecommons.org/licenses/by-nc-sa/4.0/

## The IP geolocation data is provided by
## http://www.ip2location.com

## pygmaps carries the Apache 2.0 license

import re
import os
import random
from uuid import uuid4
from flask import Flask, render_template, request
import IP2Location
import pygmaps

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024

#   Regular expression for splitting filename
spl = re.compile(
    r"(?P<ts>\d+)T"
    r"(?P<orig>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<orig_port>\d+)\-"
    r"(?P<dest>\d{3}\.\d{3}\.\d{3}\.\d{3})\.(?P<dest_port>\d+)"
)

@app.route('/')
def root():
    return '<html><body><h1>Welcome to the Manifest Data Project</h1><p><a href="/map">Please submit data here</a></p></body></html>'

@app.route('/map', methods=['GET', 'POST'])
def google_map_form():
    errors = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # if file.mimetype == 'txt/plain':
            data = file.read().split()
            output = geolocate_ips(data)
            return render_template('map_output.html', output=output)
    else:
        return render_template('file_upload.html')

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

def geolocate_ips(files):
    """
    create google map of geolocated IP addresses with paths
    connecting points
    """

    #	Initialize IP2Location obj
    locobj = IP2Location.IP2Location()
    loc_path = os.path.join(os.path.dirname(__file__),
                            '../data/IP2LOCATION-LITE-DB11.BIN')
    try:
        locobj.open(loc_path)
    except:
        raise Exception('Could not find IP2Location binary... '
                        'Make sure it is in {0}/data'.format(BASE_DIR))

    #   Creates map with a center roughly over the US
    mymap = pygmaps.maps(37.428, -122.145, 4)

    s = []
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
            h = '#%02X%02X%02X' % (r(), r(), r())
            mymap.addpath(path, h)
    output = os.path.join(os.path.dirname(__file__), 'tmp', uuid4())
    mymap.draw(output)

    #	for attribution of IP data
    with open(output, 'rb') as fi:
        html = fi.read()
        html += """
			<html>
				<body>
					<p style="text-align: center">The IP geolocation data is
					provided by <a href="http://www.ip2location.com">
					http://www.ip2location.com</a></p>
				</body>
			</html>"""
    os.unlink(output)
    return html


def geolocate(locobj, ip):
    """
    :param locobj: location object
    :param ip: ip address to be located
    :return: tuple of lat, long coordinates

    Tries to locate object, returns 0.0 if not found.
    """
    try:
        req = locobj.get_all(ip)
    except:
        return (0.0, 0.0)

    return (req.latitude, req.longitude)

if __name__ == '__main__':
    app.run(debug=True)
