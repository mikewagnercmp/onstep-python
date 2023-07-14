# OnStep Telescope Controller interface



import time
from datetime import datetime
import onstep_comm



class onstep:
  def __init__(self, host = '', port = ''):
    self.host = host
    self.port = port

    # Check what mode we are in, serial USB or over TCP/IP
    
    
    self.scope = onstep_comm.OnstepInterface(host,port)
   

    self.is_slewing = False
    self.is_tracking = False
    self.is_parked = None
    self.type = None
    self.home_wait = False
    self.is_home = None
    self.pier_side = None
    self.pec_recorded = False
    self.pec = None
    self.pps = False
    self.pulse_guide_rate = None
    self.guide_rate = None
    self.general_error = None
    self.align_Max_Stars = None
    self.align_This_Star = None
    self.align_Last_Star = None
    self.scope_aligning = None

    # TODO Need to add variables for:
    # - aligned or not
    # - number of stars aligned

    self.last_update = datetime.now()

  def close(self):
    self.scope.close()

  # Keep receiving from the port, until you get a terminating #
  def recv_message(self):
    s = self.scope.read_response()
    return s

  def get_tracking_rate(self):
    self.scope.send_command('#:GT#')
    return self.recv_message()


  def align(self, num_stars = 1):
    # Align command
    align = self.scope.send_command('#:A' + str(num_stars) + '#')
    return align

  def get_align_status(self):
    # Align command
    align_status =self.scope.send_command('#:A?#')
    if len(align_status) == 3:
        if '0' <= align_status[0] <= '9':
            self.align_Max_Stars = int(align_status[0])
        if '0' <= align_status[1] <= '9':
            self.align_This_Star = int(align_status[1])
        if '0' <= align_status[2] <= '9':
            self.align_Last_Star = int(align_status[2])
        if self.align_This_Star != 0 and self.align_This_Star <= self.align_Last_Star:
            self.scope_aligning = True
        else:
            self.scope_aligning = False
    else:
        self.align_Max_Stars = 0
        self.align_This_Star = 0
        self.align_Last_Star = 0
        self.scope_aligning = False

    return align_status

  def tracking_on(self):
    # Turn on tracking
    turn_tracking_on =self.scope.send_command('#:Te#')
    return turn_tracking_on

  def tracking_off(self):
    # Turn off tracking
    Turn_off_tracking= self.scope.send_command('#:Td#')
    return Turn_off_tracking

  def send_command_str(self, string):
    # send_command a string
    send_command_string = self.scope.send_command(string)
    return send_command_string

  def dump_status(self):
    self.update_status()
    print('Mount type:       ' + str(self.type))
    print('Slewing:          ' + str(self.is_slewing))
    print('Tracking:         ' + str(self.is_tracking))
    print('Parking:          ' + str(self.is_parked))
    print('Home:             ' + str(self.is_home))
    print('Wait Home:        ' + str(self.home_wait))
    print('Pier-side:        ' + str(self.pier_side))
    print('PEC Recorded?:    ' + str(self.pec_recorded))
    print('PEC:              ' + str(self.pec))
    print('PPS:              ' + str(self.pps))
    print('Pulse guide rate: ' + str(self.pulse_guide_rate))
    print('Guide rate:       ' + str(self.guide_rate))
    print('General error:    ' + str(self.general_error))

  def update_status(self):
    now = datetime.now()

    self.last_update = now

    s= self.scope.send_command(':GU#')
    

    if 'n' in s and 'N' in s:
      self.is_slewing = False
      self.is_tracking = False

    if not 'n' in s and not 'N' in s:
      self.is_slewing = True
      self.is_tracking = False

    if not 'n' in s and 'N' in s:
      self.is_slewing = False
      self.is_tracking = True

    if 'n' in s and not 'N' in s:
      self.is_slewing = True
      self.is_tracking = False

    if 'p' in s:
      self.is_parked = False
    if 'P' in s:
      self.is_parked = True
    if 'I' in s:
      self.is_parked = 'Parking in progress'
    if 'F' in s:
      self.is_parked = 'Parking failed'

    if 'H' in s:
      self.is_home = True
    else:
      self.is_home = False

    if 'w' in s:
      self.home_wait = True

    if 'G' in s:
      self.guide = 'Guide pulse active'

    if 'S' in s:
      self.pps = True
    else:
      self.pps = False

    if 'R' in s:
      self.pec_recorded = True
    else:
      self.pec_recorded = False

    if '/' in s:
      self.pec = 'Ignore'
    if ',' in s:
      self.pec = 'Ready to Play'
    if '~' in s:
      self.pec = 'Playing'
    if ';' in s:
      self.pec = 'Ready to Record'
    if '^' in s:
      self.pec = 'Recording'

    if 'E' in s:
      self.type = 'Equatorial'
    if 'K' in s:
      self.type = 'Fork'
    if 'k' in s:
      self.type = 'Fork Alternate'
    if 'A' in s:
      self.type = 'AltAz'

    if 'o' in s:
      self.pier_side = 'None'
    if 'T' in s:
      self.pier_side = 'East'
    if 'W' in s:
      self.pier_side = 'West'

    if len(s) > 3:
      self.pulse_guide_rate = s[-3]
      self.guide_rate = s[-2]
      self.general_error = ord(s[-1])-ord('0')

  def set_target_azm(self, azm):
    set_target_azm=self.scope.send_command(':Sz' + azm + '#')
    return set_target_azm

  def set_target_alt(self, alt):
    set_target_alt = self.scope.send_command(':Sa' + alt + '#')
    return set_target_alt
  
  def set_target_ra(self, ra):
    set_target_ra= self.scope.send_command(':Sr' + ra + '#')
    return set_target_ra

  def set_target_dec(self, de):
    set_target_dec = self.scope.send_command(':Sd' + de + '#')
    return set_target_dec

  def slew_equ(self):
    # Slew to a certain RA and DEC
    rc= self.scope.send_command(':MS#')
    
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def slew_hor(self):
    # Slew to a certain Alt and Azm
    rc = self.scope.send_command(':MA#')
    
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def slew_polar(self):
    # Slew to the assumed position for polar alignment
    rc= self.scope.send_command(':MP#')
    
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def sync(self):
    # Move back to home position TODO WTF is this
    self.update_status()
    # Sync only if the scope is tracking
    if self.is_tracking == True:
      response = "Synch Failed"
      response =self.scope.send_command(':CM#')
      
      if response =="N/A":
          response = "Sync Successful"
          return response
    else:
      return response

  def set_backlash(self, axis = 1, value = 0):
    # Set backlash for axis
    if axis == 1:
      ax = 'R'
    elif axis == 2:
      ax = 'D'
    else:
      return '0'

    set_backlash = self.scope.send_command(':$B' + ax + str(value) + '#')
    return set_backlash

  def get_backlash(self, axis = 1):
    # Get backlash for axis
    if axis == 1:
      ax = 'R'
    elif axis == 2:
      ax = 'D'
    else:
      return '0'

    get_backlash= self.scope.send_command(':%B' + str(ax) + '#')
    return get_backlash

  def get_debug_equ(self):
    # Get Equatorial values in decimal 
    get_debug_equ = self.scope.send_command(':GXFE#')
    return get_debug_equ

  def get_ax_motor_pos(self, axis = 1):
    # Get Axis motor position
    if axis == 1:
      ax = '8'
    elif axis == 2:
      ax = '9'
    else:
      return '0'

    get_ax_motor_pos = self.scope.send_command(':GXF' + str(ax) + '#')
    return get_ax_motor_pos

  def get_spd(self, axis = 1):
    # Get Axis motor position
    if axis == 1:
      ax = '4'
    elif axis == 2:
      ax = '5'
    else:
      return '0'

    get_spd = self.scope.send_command(':GXE' + str(ax) + '#')
    return get_spd

  def get_cor_alt(self):
    # Get Altitude Correction
    get_cor_alt = self.scope.send_command(':GX02#')
    return get_cor_alt

  def get_cor_azm(self):
    # Get Azimuth Correction
    get_cor_azm= self.scope.send_command(':GX03#')
    return get_cor_azm

  def get_cor_do(self):
    # Get Cone Error Correction
    get_cor_do = self.scope.send_command(':GX04#')
    return get_cor_do

  def set_utc_offset(self, utc_offset): #TODO TIme dependent
    print('Setting UTC Offset to: ' + utc_offset)
    self.scope.send_command(':SG' + utc_offset + '#')
    time.sleep(1)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_utc(self):
    # Get controller utc offset
    get_utc= self.scope.send_command(':GG#')
    return get_utc

  def set_date(self): #TODO TIme dependent
    t = datetime.now()
    date = t.strftime("%m/%d/%y")
    print('Setting date to: ' + date)
    ret = self.scope.send_command('#:SC' + date + '#')
    if ret == '1':
      return True
    else:
      return False

  def set_utcdate(self): #TODO TIme dependent
    t = datetime.utcnow()
    date = t.strftime("%m/%d/%y")
    print('Setting date to: ' + date)
    ret =self.scope.send_command(':SC' + date + '#')
    if ret == '1':
      return True
    else:
      return False
    
  def get_date(self):
    # Get controller date
    get_date = self.scope.send_command(':GC#')
    return get_date

  def set_time(self): #TODO TIme dependent 1 sec
    t = datetime.now()
    curr_time = t.strftime('%H:%M:%S')
    print('Setting time to: ' + curr_time)
    ret = self.scope.send_command(':SL' + curr_time + '#')   
    if ret == '1':
      return True
    else:
      return False

  def set_utctime(self): #TODO TIme dependent 1 sec
    t = datetime.utcnow()
    curr_time = t.strftime('%H:%M:%S')
    print('Setting time to: ' + curr_time)
    ret = self.scope.send_command(':SL' + curr_time + '#')
    if ret == '1':
      return True
    else:
      return False

  def get_time(self, high_precision = False):
    # Get controller time
    if high_precision == True:
      cmd = 'GLa'
    else:
      cmd = 'GL'
    get_time = self.scope.send_command(':' + cmd + '#')
    return get_time

  def get_sidereal_time(self, high_precision = False):
    # Get controller sidereal time
    if high_precision == True:
      cmd = 'GSa'
    else:
      cmd = 'GS'
    get_sidereal_time = self.scope.send_command(':' + cmd + '#')
    return get_sidereal_time

  def set_horizon_limit(self, limit):  # TODO add exceptions to all methods #TODO TIme dependent
    try:
      ret = self.scope.send_command(':Sh' + limit + '#')
      if ret == '1':
        return True
      else:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

  def set_overhead_limit(self, limit):
    ret = self.scope.send_command(':So' + limit + '#')
    
    if ret == '1':
      return True
    else:
      return False

  def set_longitude(self, longitude): 
    print('Setting longitude to: ' + longitude)
    ret = self.scope.send_command(':Sg' + longitude + '#', 2)
    if ret == '1':
      return True
    else:
      return False

  def get_longitude(self):
    # Get controller utc offset
    get_longitude = self.scope.send_command(':Gg#')
    return get_longitude

  def set_latitude(self, latitude): #TODO TIme dependent 2 sec
    print('Setting latitude to: ' + latitude)
    ret = self.scope.send_command(':St' + latitude + '#')
    if ret == '1':
      return True
    else:
      return False

  def get_latitude(self):
    # Get controller utc offset
    get_latitude = self.scope.send_command(':Gt#')
    return get_latitude

  def get_version(self):
    # Get OnStep version
    get_version= self.scope.send_command('#:GVN#')
    return get_version

  def get_ra(self, high_precision = False):
    # Get RA
    if high_precision == True:
      cmd = 'GRa'
    else:
      cmd = 'GR'
    self.update_status()
    get_ra = self.scope.send_command(':' + cmd + '#')
    return get_ra

  def get_dec(self):
    cmd = 'GD'
    self.update_status()
    get_dec = self.scope.send_command(':' + cmd + '#')
    return get_dec

  def get_alt(self):
    # Get Alt
    self.update_status()
    get_alt =self.scope.send_command(':GA#')
    return get_alt

  def get_azm(self):
    # Get Azm
    self.update_status()
    get_azm = self.scope.send_command(':GZ#')
    return get_azm

  def return_home(self):
    # Move back to home position
    self.update_status()
    self.scope.send_command(':hC#')

  def reset_home(self):
    # Reset, as if pointing to the home position
    self.update_status()
    self.scope.send_command(':hF#')

  def set_speed(self, speed = '20x'):
    # Set speed
    if   speed == '0.25x':
      s = '0'
    elif speed == '0.5x':
      s = '1'
    elif speed == '1x':
      s = 'G'
    elif speed == '2x':
      s = '3'
    elif speed == '4x':
      s = '4'
    elif speed == '8x':
      s = 'C'
    elif speed == '20x':
      s = 'M'
    elif speed == '48x':
      s = 'F'
    elif speed == 'half':
      s = 'S'
    elif speed == 'max':
      s = '9'
    else:
      return False

    self.scope.send_command(':R' + s + '#')
    return True

  def stop(self):
    # Stop all movememnt
    self.scope.send_command(':Q#')

  def move(self, direction = ''):
    # Move in a certain direction
    if direction == 'n' or direction == 's' or direction == 'w' or direction == 'e':
      self.scope.send_command(':M' + direction + '#')
      return True
    else:
      return False
  def un_park(self):
    response = self.scope.send_command(':hR#')
    return response

