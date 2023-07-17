ip_address = '192.168.1.27'
port = 9996
#Below are examples for units, etc. They can be set on startup
# Coordinates for the star to slew to
ra = '11:03:43'
de = '+61*45:03'

# Horizon coordinates
alt = '+45:00:00'
azm = '120:00:00'
# Location coordinates, change according to where you are
# Chardonm Ohio, USA
lat = '+41*38'
lon = '081:09'

# Offset from UTC, which is the opposite sign of the time zone
# Use +05 for EST/EDT
utc = '+05'

# Horizon and overhead limits
hor_lim = '-10'
ovh_lim = '90'

import sys
import os
sys.path.append(os.getcwd())

import onstep
# Create a scope object
scope = onstep.onstep(ip_address,port)