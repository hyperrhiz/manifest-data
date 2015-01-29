#!/bin/bash

## Author: 	Luke Caldwell
## License: Creative Commons BY-SA 3.0
##			http://creativecommons.org/licenses/by-sa/3.0/

## Setup ids for resetting file permissions
DIR=$(dirname "$0")
OUT=$DIR/.ids
id -u > $OUT
id -g >> $OUT

## Install tcpflow and link it to /usr/local/bin
sudo apt-get update && sudo apt-get install tcpflow
sudo ln -s /usr/bin/tcpflow /usr/local/bin/tcpflow
echo 'Setup complete!'