__author__ = 'Copyright (c) 2014 Dawn Robotics Ltd All rights reserved.'

"""
Copyright (c) 2014 Dawn Robotics Ltd All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


This file demonstrates how to recreate the basic blink sketch using PyMata
"""

import signal
import time

from PyMata.pymata import PyMata

# Pin 13 has an LED connected on most Arduino boards.
# give it a name:
LED = 13

# Create an instance of PyMata.
SERIAL_PORT = "/dev/ttyACM0"
firmata = PyMata( SERIAL_PORT, max_wait_time=10, firmata_type=PyMata.STANDARD_FIRMATA )

# initialize the digital pin as an output.
firmata.set_pin_mode( LED, firmata.OUTPUT, firmata.DIGITAL )

try:
    # run in a loop over and over again forever:
    while True:
        
        firmata.digital_write( LED, firmata.HIGH )   # turn the LED on (HIGH is the voltage level)
        time.sleep( 1.0 );                           # wait for a second
        firmata.digital_write( LED, firmata.LOW )    # turn the LED off by making the voltage LOW
        time.sleep( 1.0 );                           # wait for a second

except KeyboardInterrupt:

    # Catch exception raised by using Ctrl+C to quit
    pass

# close the interface down cleanly
firmata.close()


