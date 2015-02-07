## Author: 	Luke Caldwell
## Org: Duke University S-1 Speculative Sensation Lab
## Website: http://s-1lab.org
## License: Creative Commons BY-NC-SA 4.0
##			http://creativecommons.org/licenses/by-nc-sa/4.0/

## The IP geolocation data is provided by
## http://www.ip2location.com

## pygmaps carries the Apache 2.0 license

import os
import re
import random
from uuid import uuid4
import glob
from flask import Flask, render_template, request, send_from_directory
import IP2Location
import pygmaps

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
app.config['STATIC_FILES'] = os.path.join(os.path.dirname(__file__), 'static')
app.config['GAL_DIR'] = os.path.join(app.config['STATIC_FILES'], 'gallery')


@app.route('/')
def root():
    return '<html><body><h1>Welcome to the Manifest Data Project</h1><p><a href="/map">Please submit data here</a></p></body></html>'

@app.route('/map', methods=['GET', 'POST'])
def google_map_form():
    errors = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            keep = request.form.get('keep')
            data = file.read().split()
            output = geolocate_ips(data, keep)
            return render_template('map_output.html', output=output)
    else:
        return render_template('file_upload.html')

@app.route('/gallery')
def map_gallery():
    gal_dir = os.path.join(app.config['GAL_DIR'], '*.html')
    print(gal_dir)
    files = [os.path.basename(f) for f in glob.glob(gal_dir)]
    return render_template('gallery.html', links=files)


regex_validator = re.compile('^{r}\.{r}\.{r}\.{r},'
                             '{r}\.{r}\.{r}\.{r}$'.format(r='\d{1,3}')
)

# @app.route('/gallery/<path:filename>')
# def serve_static_map(filename):
#     print(app.config['GAL_DIR'])
#     return send_from_directory(app.config['GAL_DIR'], filename)


def geolocate_ips(files, keep):
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
        raise Exception('Could not find IP2Location binary... ')

    #   Creates map with a center roughly over the US
    mymap = pygmaps.maps(37.428, -122.145, 4)

    s = []
    for f in files:
        if not regex_validator.search(f):
            continue
        orig, dest = f.split(',')
        orig_latlong = geolocate(locobj, orig)
        dest_latlong = geolocate(locobj, dest)
        out = [orig_latlong, dest_latlong]
        s.append(out)
    for path in s:
        if (0.0, 0.0) not in path:
            #	sets random hex color for gmaps path
            r = lambda: random.randint(0, 255)
            h = '#%02X%02X%02X' % (r(), r(), r())
            mymap.addpath(path, h)
    addendum = """
                <html>
                    <body>
                        <p style="text-align: center">The IP geolocation data is
                        provided by <a href="http://www.ip2location.com">
                        http://www.ip2location.com</a></p>
                    </body>
                </html>"""
    if keep:
        output = os.path.join(app.config['GAL_DIR'],
                              str(uuid4()) + '.html')
        mymap.draw(output)
        #	for attribution of IP data
        with open(output, 'ab') as fi:
            fi.write(addendum)
        with open(output, 'rb') as fi:
            html = fi.read()
    else:
        output = os.path.join(os.path.dirname(__file__), 'tmp', str(uuid4()))
        mymap.draw(output)

        #	for attribution of IP data
        with open(output, 'rb') as fi:
            html = fi.read()
            html += addendum
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
    app.run()
