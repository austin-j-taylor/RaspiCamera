from picamera import PiCamera
from time import sleep, strftime
import os, logging
camera = PiCamera()

# Time to wait between photos are taken (seconds)
TIMELAPSE_WAIT_S = 60
# Where to save the photos and log file
# Make sure the USB drive is mounted to /mnt/photo-drive/ and the user has the right permissions
SAVE_LOCATION = "/mnt/photo-drive/"
# Root directory of the device (e.g. USB drive) where the photos are saved
# Used to calculate how much available space there is before stopping
SAVE_LOCATION_ROOT = "/mnt/photo-drive/"


captureDirectory = SAVE_LOCATION + "captures/"
try:
    logging.basicConfig(filename=SAVE_LOCATION +'photos.log', level=logging.DEBUG)
except FileNotFoundError:
    print("Storage device was not connected.")
    exit()


camera.rotation = 180
# How full the sd card should be before stopping taking pictures
capacity_full = 95


# Log device storage space information
info = os.statvfs(SAVE_LOCATION_ROOT)
logging.debug(info)
print(info)

# Create captures folder if necessary
try:
    os.mkdir(captureDirectory)
    print("created directory: " + captureDirectory)
except:
    pass

# Returns how full the storage device is as a percentage
def system_capacity():
    global info
    info = os.statvfs(SAVE_LOCATION_ROOT)
    return info.f_bavail / info.f_blocks

# Main loop
while(True):
    # One folder for each day
    dayString = strftime("%m_%d_%Y")
    folder = captureDirectory + dayString + "/"
    filename = dayString + strftime("__%H-%M-%S") + ".jpg"
    try:
        os.mkdir(folder)
    except:
        pass
    # Take the photo, save it
    camera.capture(folder + filename)
    logging.debug(folder + filename)
    
    # Upload to dropbox
    #print(os.system('./dbxcli put ' + folder + filename + ' /Apps/PiCameraTaylor/' + filename))
    
    # Check storage device usage and shut down when too full
    capacity = 100 - int(system_capacity() * 100)
    logging.debug(str(capacity) + "%")
    if(capacity >= capacity_full):
        logging.debug("Data storage device is full. Shutting down.")
        os.system("sudo poweroff")
        exit()
    
    
    sleep (TIMELAPSE_WAIT_S)

    