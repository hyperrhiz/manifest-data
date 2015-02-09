Luke Caldwell

Manifest Data

Duke University S-1 Speculative Sensation Lab

[http://s-1lab.org](http://s-1lab.org)

License: Creative Commons BY-NC-SA 4.0 [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)

This project uses geolocation data derived from [http://www.ip2location.com](http://www.ip2location.com).

This project also uses pygmaps, distributed under the Apache 2.0 license.
---------------------------------------------------------------------------------------------------------------------------
DMG installer
--------------
FOR MAC ONLY

Installation
-------------
To install tcpflow and scripts for this project download and mount [the DMG installer](https://bitbucket.org/swibble/manifest-data/downloads/manifest-data.dmg). Open a terminal and enter the following command:
sh /Volumes/MANIFESTD/install.sh

You will be prompted to enter your password for the install to proceed.

You will also need to install the X11 framework. You can download it here.
[http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.5.dmg](http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.5.dmg)

--------------------------------------------------------------------------------------------------------------
## Linux Installation ##

Install git

```
sudo apt-get update && sudo apt-get -y install git
```
Clone repository
```
git clone https://bitbucket.org/swibble/manifest-data ~/manifest-data
```
Run ~/manifest-data/linux_setup.sh

This will install tcpflow and other dependencies.

--------------------------------------------------------------------------------------------------------------


Running
-------------
Open a terminal and run the following command:
```
sudo python /Applications/Manifest_Data/manifest_data.py
```
or
```
sudo python /path/to/manifest-data/manifest_data.py
```
You will be prompted to enter your admin password every time you run this. This will create a folder called "tcpflow" in the application directory where it will save all the files. You can delete these whenever you want.

Additional options:

* -o = set custom output folder for tcpflow data

-----------------------------------------------------

Parsing
------------
To parse the IP addresses from the files, run the following command in a terminal:
```
python /Applications/Manifest_Data/parse_data.py
```
or
```
python ~/manifest-data/parse_data.py -t
```

You have two options for parsing the data. Running with defaults creates a .xyz file that can be used to create a 3D model. Adding the -t flag will output a text file that can be uploaded at the [Manifest Data project page](http://s-1lab.org/project/manifest-data/#upload) to display a Google map of your connections.

Additional options:

* -o = specify custom output filename

* -i = specify custom tcpflow input directory

* -v = prints out more information