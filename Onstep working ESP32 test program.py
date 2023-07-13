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

def report():

  # Display date, time, UTC offset, and latitude/longitude
  dt  = config.scope.get_date()
  tm  = config.scope.get_time()
  ut  = config.scope.get_utc()
  lt  = config.scope.get_latitude()
  lg  = config.scope.get_longitude()
  lst = config.scope.get_sidereal_time()
  print('Date: %s Time: %s UTC %s Lat: %s Long: %s LST: %s' % (dt, tm, ut, lt, lg, lst))

  print('Time     Stat Mnt-Time RA       DEC       Alt       Azm      ')
  while True:

    scope_tm = config.scope.get_time()
    dt = datetime.now().strftime('%H:%M:%S')

    curr_ra = config.scope.get_ra()
    curr_de = config.scope.get_dec()
    curr_alt = config.scope.get_alt()
    curr_azm = config.scope.get_azm()

    status = '---'
    if config.scope.is_slewing is True:
      status = 'SLW'
      
    if config.scope.is_tracking is True:
      status = 'TRK'

    if config.scope.is_home is True:
      status = 'HOM'

    print('%s %s  %s %s %s %s %s' % (dt, status, scope_tm, curr_ra, curr_de, curr_alt, curr_azm))
    
    
    return

def run_onstep_terminal():
    #onstep = OnstepInterface.OnstepInterface()
    #onstep = config.scope
    loop_counter = 0
    error_counter =0 

    try:
        while True:
            try:
                s = config.scope.dump_status()
                print( "\n")
            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")

            try:
                s = config.scope.get_utc()
                print(f"Time {s}\n")
            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")

            try:
                s = config.scope.get_ra()
                print(f"RA {s}\n")
            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")

            
            try:
                s = config.scope.get_dec()
                print(f"DEC {s}\n")
            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")

            try:
                report()
            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")


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
