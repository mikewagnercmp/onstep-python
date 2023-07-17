# onstep-python
Fault-tolerant socket-based Python communication protocol for Onstep and other LX200 telescopes.

Based on the excellent work here: https://github.com/kbahey/onstep-python - He did all the hard work to decipher and code up methods for the LX200 protocol and commands, and it would have taken me forever to do that myself.

The existing Onstep Python library was written a while ago, prior to some major architecture changes and new supported chips like the ESP32. The old library would run into issues as the socket would time out. Once that happened, you would have to reconnect and so on.

The new code has a modified comms class that sets a socket timeout, retries, and has reasonable exception handling. The previous way of sending/receiving as two separate methods was also inefficient, as in some cases the socket could be closed. Now the same connection is reused for sending commands and receiving responses. Where a command may require more time to process on Onstep, a delay parameter can optionally be passed in.

This is set up to be used as an IP/network protocol only - I have not rewritten the TTY connection method as I have no real use for it.

There is a test program included that can loop some data requests from the scope. I was using this to test performance and error handling, especially with regard to the ESP32 chips. If more than one client was connected to the Onstep SWS, the number of socket timeouts and errors would dramatically increase. With the new connection code, I was able to get a 100% response to all commands.

# Usage
To configure, modify the config.py file to have the correct IP address of your Onstep scope. Set a port in the range of 9996-9999. Run the test program, and you should see some basic info returns such as the status, RA/Dec, etc.

The working test program will unpark the scope, slew to a circumpolar star, set some incorrect offset coordinates simulating a bad goto, and then sync the scope on the coordinates. Once the sync happens, the scope will then slew to the target, presumably more accurate now that there is a local sync point.

The Onstep alignment test program goes through the steps of building a proper alignment model. It unparks the scope, sets the alignment to a 3-star alignment, and then go-to's a star and does a sync similar to the first test program. However, in this case, the sync will create an alignment point as we are in align mode. This process is repeated 2 more times until the alignment is complete.