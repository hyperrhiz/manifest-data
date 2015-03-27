Luke Caldwell

Manifest Data

Duke University S-1 Speculative Sensation Lab

[http://s-1lab.org/project/manifest-data/](http://s-1lab.org/project/manifest-data/)

License: Creative Commons BY-NC-SA 4.0 [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)

This project uses geolocation data derived from [http://www.ip2location.com](http://www.ip2location.com).

This project also uses pygmaps, distributed under the Apache 2.0 license.

--------------------------------------------------------------------------------------------------------------
## tcpflow ##

This project relies upon the [tcpflow](http://manpages.ubuntu.com/manpages/hardy/man1/tcpflow.1.html) networking utility to collect networking data locally on your machine. When running, tcpflow will collect the content and metadata associated with all networking calls your computer makes. 

## Privacy ##
The information this program collects is potentially sensitive. Networking connections that utilize SSL will be stored in an encrypted state, but will reveal other metadata such as IP addresses, mime-type, timestamp, and filesize.

This information is not transmitted to anyone and is stored locally on your machine in a default folder called "tcpflow." Feel free to remove this folder when your experiments are complete.

The only information that is transmitted to us is if you choose to create a Google map of your connections. This will involve sending a list of IP addresses to the S-1lab.org server where the IP addresses will be geolocated and mapped. The original file with the IP addresses will not be saved. If you choose to save your Google map to our public gallery, your map is assigned an anonymous identifier. The maps include only the GPS coordinates for your networking connections, not any IP address or timestamp information.

If you would like to examine the server code used to generate the maps (using Flask), you can find it in Source --> manifest-data --> __init__.py 

--------------------------------------------------------------------------------------------------------------
## OS X Installation ##

To install tcpflow and scripts for this project download and mount [the DMG installer](https://bitbucket.org/swibble/manifest-data/downloads/manifest-data.dmg). Open a terminal and enter the following command:
```
sh /Volumes/MANIFESTD/install.sh
```
You will be prompted to enter your password for the install to proceed.

**You will also need to install the X11 framework**. You can [download it here](http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.5.dmg).

install.sh copies the following libraries necessary for tcpflow to run:

* libcairo.2.dylib
* libfontconfig.1.dylib
* libfreetype.6.dylib
* libpixman-1.0.dylib
* libpng15.15.dylib

These files are all copied to /usr/local/lib/.

tcpflow is copied to /usr/local/bin/.

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
Run 
```
sh ~/manifest-data/linux_setup.sh
```

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

##Important:##
When you wish to stop collection, make sure to **go to the terminal window and press ctrl-c**. If you do not, you will encounter problems parsing the data that you have collected.

When you switch locations, you should also close the script with ctrl-c and restart it.

If you close the window without hitting ctrl-c, all files will be owned by root rather than by your user, making them impossible to read without changing file permissions. Also, the IP address data will be corrupted and will contain internal IP addresses rather than external ones, making them impossible to geolocate.

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