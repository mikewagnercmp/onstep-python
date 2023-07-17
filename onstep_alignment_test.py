# Onstep working ESP32 test program
#import onstep_comm as OnstepInterface
import config
import time
import sys
import socket
from datetime import datetime
import onstep_utils


# Common stars, used the coordinates of one of them below
stars_coordinates = {
    "Mothalah":     {"RA": "01:54:10", "Dec": "+29*40:12"},
    "Beta Bootis":  {"RA": "15:01:56", "Dec": "+40*23:25"},
    "Rasalhague":   {"RA": "17:34:56", "Dec": "+12*33:31"},
    "Vega":         {"RA": "18:36:56", "Dec": "+38*47:06"},
    "Deneb":        {"RA": "20:41:25", "Dec": "+45*16:49"},
    "Eps Cygn":     {"RA": "20:46:13", "Dec": "+33*58:19"},
    "Alpheratz":    {"RA": "23:04:45", "Dec": "+15*12:18"},
    "Hamal":        {"RA": "02:07:11", "Dec": "+23*27:42"},
    "Algol":        {"RA": "03:08:10", "Dec": "+40*57:20"},
    "Aldebaran":    {"RA": "04:35:55", "Dec": "+16*30:29"},
    "Menkalinan":   {"RA": "05:59:31", "Dec": "+44*56:50"},
    "Mintaka":      {"RA": "05:32:00", "Dec": "-00*17:56"}, # On the celestial equator
    "Zawijah":      {"RA": "11:50:41", "Dec": "+01*45:55"}, # Almost on the celestial equator
    "Alkaid":       {"RA": "13:47:32", "Dec": "+49*18:48"}, # Circumpolar for most of northern latitudes
    "Dubhe":        {"RA": "11:03:43", "Dec": "+61*45:03"}, # Circumpolar for most of northern latitudes
    "Aldhibah":     {"RA": "17:08:51", "Dec": "+65:41:01"},  #Also circumpolar
    "Aldhibah_Wrong":     {"RA": "17:20:51", "Dec": "+65:01:01"},
    "Alkaid_Wrong":       {"RA": "13:40:32", "Dec": "+49*20:48"}
}

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

                #Begin Align point 1

                ans = input("\n hit any key to enter alignment mode , Star 1\n")
                config.scope.align(1)
                onstep_utils.print_alingment_status()
                print("set coordinates for Aldhibah - its circumpolar")
                config.scope.set_target_ra(stars_coordinates["Aldhibah"]["RA"])
                config.scope.set_target_dec(stars_coordinates["Aldhibah"]["Dec"])
                config.scope.slew_equ()
                
                
                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(1)
                    config.scope.update_status()
                    onstep_utils.report()

                print("target set, lets check \n")
                onstep_utils.report()
                ans = input("lets now send some different coordinate, check the planetarium")
                config.scope.set_target_ra(stars_coordinates["Aldhibah_Wrong"]["RA"])
                config.scope.set_target_dec(stars_coordinates["Aldhibah_Wrong"]["Dec"])

                print("Lets sync \n")
                s = config.scope.sync()
                
                print(f"synch response {s}\n")
                
                
                onstep_utils.print_alingment_status()
                ans = input("Alignment point should be accepted. Check \n")

                #   End of align point 1
                #   Begin align point 2

                ans = input("\n hit any key to enter alignment mode , Star 2\n")
                config.scope.align(2)
                onstep_utils.print_alingment_status()
                print("set coordinates for Aldhibah - its circumpolar")
                config.scope.set_target_ra(stars_coordinates["Alkaid"]["RA"])
                config.scope.set_target_dec(stars_coordinates["Alkaid"]["Dec"])
                config.scope.slew_equ()
                
                
                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(1)
                    config.scope.update_status()
                    onstep_utils.report()

                print("target set, lets check \n")
                onstep_utils.report()
                ans = input("lets now send some different coordinate, check the planetarium")
                config.scope.set_target_ra(stars_coordinates["Alkaid_Wrong"]["RA"])
                config.scope.set_target_dec(stars_coordinates["Alkaid_Wrong"]["Dec"])

                print("Lets sync \n")
                s = config.scope.sync()
                
                print(f"synch response {s}\n")
                
                
                onstep_utils.print_alingment_status()
                ans = input("Alignment point should be accepted. Check \n")
                

                print("Lets park")
                p = config.scope.move_to_park()
                print(f"Parking status - {p}\n")

                config.scope.update_status()
                while config.scope.is_slewing == True:
                    print("scope is slewing \n")
                    time.sleep(.5)
                    config.scope.update_status()
                    onstep_utils.report()
                
                config.scope.update_status()
                print("Scope parking status is "+ str(config.scope.is_parked))


            except Exception as e:
                error_counter +=1
                print(f"Caught an exception: {e}")    


            loop_counter += 1
            print(f"\n\nLoop has run successfully {loop_counter} times. and had {error_counter} errors")
            
            

            if loop_counter == 1:
                do_exit()
    except (socket.error, KeyboardInterrupt) as e:
        print(f"Caught exception: {e}. Attempting to reconnect in 5 seconds...")
        do_exit()
    finally:
        do_exit()



run_onstep_terminal()