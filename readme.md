Luke Caldwell

Manifest Data

Duke University S-1 Speculative Sensation Lab

[http://s-1lab.org](http://s-1lab.org)

License: Creative Commons BY-SA 3.0 [http://creativecommons.org/licenses/by-sa/3.0/](http://creativecommons.org/licenses/by-sa/3.0/)

This project uses geolocation data derived from [http://www.ip2location.com](http://www.ip2location.com).

This project also uses pygmaps, distributed under the Apache 2.0 license.

DMG installer
--------------
FOR MAC ONLY

Installation
-------------
To install tcpflow and scripts for this project open a terminal and enter the following command:
sh /Volumes/TCPFLOW/install.sh

You will be prompted to enter your password for the install to proceed.

You will also need to install the X11 framework. You can download it here.
http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.5.dmg

-----------------------------------------------------

Running
-------------
Open a terminal and run the following command:
sudo python /Applications/Manifest_Data/manifest_data.py

You will be prompted to enter your admin password every time you run this. This will create a folder called "tcpflow" in the application directory where it will save all the files. You can delete these whenever you want.
-----------------------------------------------------

Parsing
------------
To parse the IP addresses from the files, run the following command in a terminal:
python /Applications/Manifest_Data/parse_data.py

You have two options for parsing the data. Running it like this creates a .xyz file that can be used to create a 3D model. Adding the -g flag will attempt to geolocate the IP addresses and output an html file with a google map in it. This requires that you download the database from [https://lite.ip2location.com/database-ip-country-region-city-latitude-longitude-zipcode-timezone](https://lite.ip2location.com/database-ip-country-region-city-latitude-longitude-zipcode-timezone)

Additional options:
-o = specify custom output filename
-i = specify custom tcpflow input directory
-v = prints out more information
