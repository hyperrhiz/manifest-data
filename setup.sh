#!/bin/bash

## Author: 	Luke Caldwell
## License: Creative Commons BY-SA 3.0
##			http://creativecommons.org/licenses/by-sa/3.0/

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT=$DIR/.ids
id -u > $OUT
id -g >> $OUT
echo 'Setup complete!'