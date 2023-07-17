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
                print("Scope parking status is "+ str(config.scope.is_parked))
                print(f"Lets try  unpark first\n")
                config.scope.un_park()
                print("did the scope unpark \n")
                print("Scope parking status is "+ str(config.scope.is_parked))

                print("set coordinates for Aldhibah - its circumpolar")
                config.scope.set_target_ra("17:08:51")
                config.scope.set_target_dec("+65:41:01")
                config.scope.slew_equ()
                
                
                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(.5)
                    config.scope.update_status()
                    report()

                print("target set, lets chek \n")
                report()
                ans = input("lets now send some different coordinate, check the planetarium")
                config.scope.set_target_ra("17:20:51")
                config.scope.set_target_dec("+65:01:01")

                print("Lets sync ")
                s = config.scope.sync()
                print(f"synch response {s}\n")

                ans = input("we just synched to coordinates slighlty off of the target.Now we will slew to the original coordinates") 

                config.scope.set_target_ra("17:08:51")
                config.scope.set_target_dec("+65:41:01")
                config.scope.slew_equ()
                
                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(.5)
                    config.scope.update_status()
                    report()
                
                

                ans = input("Scope should have slewed back to the correct target. We will now park")

                print("Lets park")
                p = config.scope.move_to_park()
                print(f"Parking status - {p}\n")

                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(.5)
                    config.scope.update_status()
                    report()
                
                config.scope.update_status()
                print("Scope parking status is "+ str(config.scope.is_parked))


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
