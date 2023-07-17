# Onstep working ESP32 test program
#import onstep_comm as OnstepInterface
#import config
import time
import sys
from datetime import datetime
import config


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

def print_alingment_status():
  config.scope.get_align_status()
  print('Align max stars: ' + str(config.scope.align_Max_Stars))
  print('Align this star: ' + str(config.scope.align_This_Star))
  print('Align last star: ' + str(config.scope.align_Last_Star))
  print('scope aligning: ' + str(config.scope.scope_aligning))

  return