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
import datetime
from uuid import uuid4
import glob
from flask import Flask, render_template, request, send_from_directory, redirect
import IP2Location
import pygmaps

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
app.config['STATIC_FILES'] = os.path.join(os.path.dirname(__file__), 'static')
app.config['GAL_DIR'] = os.path.join(app.config['STATIC_FILES'], 'gallery')


class GalleryFile():

    def __init__(self, fn):
        self.link = os.path.basename(fn)
        self.time = time_format(fn)


@app.route('/')
def root():
    return '<html><body><h1>Welcome to the Manifest Data Project</h1><p><a href="/map">Please submit data here</a></p></body></html>'


@app.route('/map', methods=['GET', 'POST'])
def google_map_form():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            keep = request.form.get('keep')
            data = file.read().split()
            output = geolocate_ips(data, keep)
            if output.startswith('<html>'):
                return render_template('map_output.html', output=output)
            elif output.startswith('http'):
                return redirect(output)
    else:
        return render_template('file_upload.html')


@app.route('/gallery')
def map_gallery():
    gal_dir = os.path.join(app.config['GAL_DIR'], '*.html')
    print(gal_dir)
    files = [GalleryFile(f) for f in glob.glob(gal_dir)]
    return render_template('gallery.html', links=files)


regex_validator = re.compile('^{r}\.{r}\.{r}\.{r},'
                             '{r}\.{r}\.{r}\.{r}$'.format(r='\d{1,3}')
                             )


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

    #   saving to the gallery,
    #   returns url for redirect
    if keep:
        unique_string = str(uuid4()) + '.html'
        url_out = os.path.join('http://manifest.s-1lab.org/static/gallery/',
                               unique_string)
        output = os.path.join(app.config['GAL_DIR'],
                              unique_string)
        mymap.draw(output)
        #	for attribution of IP data
        with open(output, 'ab') as fi:
            fi.write(addendum)
        html = url_out

    #   create tmp file and return contents and delete
    else:
        output = os.path.join(os.path.dirname(__file__), 'tmp', str(uuid4()))
        mymap.draw(output)

        #	for attribution of IP data
        with open(output, 'rb') as fi:
            html = fi.read()
            html += addendum
        os.unlink(output)
    return html


def time_format(f):
    mtime = os.stat.ST_MTIME(f)
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime('%b %d %Y, %I:%M %p')


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
