# Functions to handle the network

from subprocess import check_output, run, PIPE
import os

# Get the current ssid
def getSSID():
    try:
        scanoutput = check_output(["iwgetid -r"], shell=True)
        #scanoutput = check_output(["iw dev"])
        ssid = "WiFi not found"

        for line in scanoutput.split():
            ssid = line.decode("utf-8")

            #if "ssid" in line:
            #    ssid = line[line.find("ssid")+5:]

            #if line[:5]  == "ESSID":
            #    ssid = line.split('"')[1]

        return (str(ssid), None)
    except Exception as e:
        return ("Wifi not set", str(e))

# Check if the network is present by pinging Google
def checkNetwork():
    hostname = "google.com" 
    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
        return True
    else:
        return False

# Set the wifi ssid and password
# Hack: run these lines before
# sudo chmod a+r /etc/wpa_supplicant/wpa_supplicant.conf
# sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf
#https://maskaravivek.medium.com/python-script-to-configure-wifi-on-raspberry-pi-without-reboot-3af07368b3c2
def setWifi(ssid, password):
    # Contents to put in wpa_supplication.conf
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=GB',
        '\n',
        'network={',
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)
    
    # Set up read/write access to file
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    
    # Write the file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
    
    print("Wifi config added. Refreshing configs")
    ## Refresh the wifi connection
    os.popen("sudo wpa_cli -i wlan0 reconfigure")


# Get settings from a wifi.txt file on a USB drive
# First line in file is ssid
# Second line is password
def getSettings():
    mediaDir = "/media/pi/"
    #mediaDir = "/"

    # Find USB drives connected
    dirs = [f for f in os.listdir(mediaDir) if os.path.isdir(mediaDir+f)]

    print("USB drives", dirs)

    if len(dirs)==0:
       return "No USB Drives Found"

    configFile = mediaDir + dirs[0] + "/wifi.txt"

    if not os.path.isfile(configFile):
       return "No wifi.txt config file found on SD card " + dirs[0]
           
    # Read config file
    with open(configFile, "r") as conf:
        lines = conf.readlines()

    if len(lines)<2:
        return "Invalid wifi.txt config file"

    return (lines[0].strip(), lines[1].strip())

def updateSoftwareFromGuthub():
    process = run('/home/pi/update_from_github.sh',
                                    shell=True,
                                    stdout=PIPE, 
                                    stderr=PIPE,
                                    universal_newlines=True)
    print("Stdout\n", process.stdout)
    print("Stderr\n", process.stderr, len(process.stderr))
    if len(process.stderr)>0:
        return ("Failed ", process.stderr[:15])
    else:
        return ("Updated", None)