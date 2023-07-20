import time
import socket
import math
import ephem
import onstep_utils
import config
import sys



# List of stars to use for alignment
alignment_stars = ["Alpheratz", "Caph", "Algenib",  "Mirach", "Achernar",
                   "Hamal", "Mirfak", "Aldebaran", "Rigel", "Capella",
                   "Betelgeuse", "Canopus", "Sirius", "Castor", "Procyon",
                   "Pollux", "Suhail", "Alphard", "Regulus", "Dubhe",
                   "Denebola", "Acrux", "Mimosa", "Mizar", "Spica", "Hadar",
                   "Arcturus",  "Alphecca", "Antares",
                   "Rasalhague", "Vega", "Albireo", "Altair", "Peacock",
                   "Deneb", "Fomalhaut", "Scheat"]

# Minimum altitude for stars (20 degrees converted to radians)
min_alt = 20 * math.pi / 180

def do_exit():
  config.scope.close()
  sys.exit()

def dms_to_decimal(dms_str):
    # Check if the input is in latitude or longitude format
    if '*' in dms_str:
        deg, min = dms_str.split('*')
    else:
        deg, min = dms_str.split(':')

    # Remove possible sign from degree part
    sign = -1 if deg[0] == '-' else 1
    deg = deg.lstrip('-+')

    # Convert to decimal format
    decimal_deg = sign * (float(deg) + float(min) / 60)

    return decimal_deg


def format_ra(ra):
    # Convert RA from radians to hours
    ra = math.degrees(ra) / 15.0
    hh, mm = divmod(ra, 1)
    mm, ss = divmod(mm * 60, 1)
    ss = round(ss * 60)
    return f"{hh:02.0f}:{mm:02.0f}:{ss:02.0f}"

def format_dec(dec):
    # Convert Dec from radians to degrees
    dec = math.degrees(dec)
    if dec < 0:
        dec = abs(dec)
        sign = "-"
    else:
        sign = "+"
    hh, mm = divmod(dec, 1)
    mm, ss = divmod(mm * 60, 1)
    ss = round(ss * 60)
    return f"{sign}{hh:02.0f}*{mm:02.0f}'{ss:02.0f}"

def get_alignment_points():
    alignment_points = []
    for star_name in alignment_stars:
        try:
            # Get the star object
            star = ephem.star(star_name)

            # Compute the star's position for the current time
            star.compute(observer)

            # Check if the star is above the minimum altitude
            if star.alt > min_alt:
                alignment_points.append(star)
                if len(alignment_points) == 9:
                    break
        except Exception as e:
            print(f"Caught an exception while computing star {star_name}: {e}")
    return alignment_points

def generate_wrong_coordinates(ra, dec):
    # Add a small offset to RA and Dec
    ra_wrong = math.degrees(ra) + 0.1
    dec_wrong = math.degrees(dec) + 0.1

    # Format RA and Dec
    ra_wrong = format_ra(ra_wrong * math.pi / 180)
    dec_wrong = format_dec(dec_wrong * math.pi / 180)

    return ra_wrong, dec_wrong

def perform_alignment(star):
    print(f"\nAligning to {star.name}")
    #input("\nHit any key to enter alignment mode\n")
    onstep_utils.print_alingment_status()

    # Set target coordinates
    print(f"Setting coordinates for {star.name}")
    ra = format_ra(star.ra)
    dec = format_dec(star.dec)
    config.scope.set_target_ra(ra)
    config.scope.set_target_dec(dec)
    config.scope.slew_equ()

    # Wait for the scope to finish slewing
    config.scope.update_status()
    while config.scope.is_slewing:
        while config.scope.is_slewing == True:
            print("scope is slewing \n")
            time.sleep(1)
            config.scope.update_status()

    print("Goto complete, scope should be at target, check in planetarium")
    onstep_utils.report()

    # Generate wrong coordinates and simulate a plate solve
    ra_wrong, dec_wrong = generate_wrong_coordinates(star.ra, star.dec)
    #input("Let's now send some different coordinates simulating a plate solve, check the planetarium")
    config.scope.set_target_ra(ra_wrong)
    config.scope.set_target_dec(dec_wrong)

    print("\nLet's sync")
    s = config.scope.sync()
    print(f"Sync response: {s}")
    onstep_utils.print_alingment_status()
    #input("Alignment point should be accepted. Check the planetarium\n")

def park_scope():
    print("\n Lets park\n")
    p = config.scope.move_to_park()
    print(f"Parking status - {p}\n")

    config.scope.update_status()
    while config.scope.is_slewing == True:
        print("scope is slewing \n")
        time.sleep(.5)
        config.scope.update_status()
        
    
    config.scope.update_status()
    print("Scope parking status is "+ str(config.scope.is_parked))

def unpark_scope():
    print("Scope parking status is "+ str(config.scope.is_parked))
    print(f"Lets try  unpark first\n")
    config.scope.un_park()
    print("did the scope unpark \n")
    print("Scope parking status is "+ str(config.scope.is_parked))


def run_onstep_terminal():
    try:
        

        unpark_scope()
        # Get the list of alignment points
        alignment_points = get_alignment_points()

        # Perform alignment for each star
        config.scope.align(len(alignment_points))
        print(f"There are {len(alignment_points)} alignment points.")

        for star in alignment_points:
            perform_alignment(star)

        
    except (socket.error, KeyboardInterrupt) as e:
        print(f"Caught exception: {e}. Attempting to reconnect in 5 seconds...")
        do_exit()
    finally:
        do_exit() 

# Provided latitude and longitude
lat_str = config.lat
lon_str = config.lon

# Convert to decimal degrees
lat = dms_to_decimal(lat_str)
lon = dms_to_decimal(lon_str)

# Create an observer object for your location
observer = ephem.Observer()
observer.lat = str(lat)  # latitude
observer.lon = str(lon)  # longitude



run_onstep_terminal()
