#!/bin/bash

## Author: 	Luke Caldwell
## License: Creative Commons BY-NC-SA 4.0
##			http://creativecommons.org/licenses/by-nc-sa/4.0/

## Setup ids for resetting file permissions
DIR=$(dirname "$0")
OUT=$DIR/.ids
id -u > $OUT
id -g >> $OUT

## Install tcpflow and link it to /usr/local/bin
sudo apt-get update && sudo apt-get install tcpflow
echo 'Setup complete!'