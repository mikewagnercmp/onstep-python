ip_address = '192.168.1.27'
port = 9996

import sys
import os
sys.path.append(os.getcwd())

import onstep
# Create a scope object
scope = onstep.onstep(ip_address,port)