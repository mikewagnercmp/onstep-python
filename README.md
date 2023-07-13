# onstep-python
Fault Tolerant socket based Python communication protocol for Onstep and other LX200 telescopes

Based on the excellent work here https://github.com/kbahey/onstep-python - He did all the hard work to decipher and code up methods for the LX200 protocol and commands and it would have taken me forever to do that myself.

The existing Onstep python library was written a while ago, prior to some maor architecture changes and new supported chips like the ESP32. The old library would run into issues as socket would time out, once that happened you would have to reconnect and so on. 

New code has a modified comms class that sets a socket timeout, retries, and has reasonable exception handling. The previous way of sending / recieving as too seperate methods also was inefficient, as in some cases the socket could e closed - now the same connection is reused for sendig commands and receiving responses. Where a command may require more time to process on Onsetp, a delay parameter can optionally be passed in.

This is set up to be used as a IP/ network protocol only - I have not rewritten the TTY connection method as I have no real use for it. 

There is a test program included that can loop some data requests from the scope. I was using this to test performance and error handling, as especialy with regard to the ESP32 chips, if more than one client was connected to the Onstep SWS the number of socket timeouts and errors would dramatically increase. With the new connection code, I was able to get a 100% response to all commands.


* Usage *
  To configure, modify the config.py file to have the correct IP address of your Onstep scopee. Set a port in the range of 9996-9999. run the test program, you should see some basica info returns such as the status, RA/Dec, etc.

  
