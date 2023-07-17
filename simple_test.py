# Onstep working ESP32 test program
#import onstep_comm as OnstepInterface
import config
import time
import sys
import socket
from datetime import datetime

def do_exit():
  config.scope.close()
  sys.exit()


def run_onstep_terminal():
    #onstep = OnstepInterface.OnstepInterface()
    #onstep = config.scope
    loop_counter = 0
    error_counter =0 

    try:
        while True:
            s= config.scope.get_tracking_rate()
            print(f"tracking rate {s}\n")
 
                
           
            loop_counter += 1
            print(f"\n\nLoop has run successfully {loop_counter} times. and had {error_counter} errors")
            #time.sleep(12)
            

            if loop_counter == 1:
                do_exit()
    except (socket.error, KeyboardInterrupt) as e:
        print(f"Caught exception: {e}. Attempting to reconnect in 5 seconds...")
        do_exit()
    finally:
        do_exit()



run_onstep_terminal()
