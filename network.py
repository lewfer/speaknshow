from subprocess import check_output
import os

# Get the current ssid
def getSSID():
    scanoutput = check_output(["iwgetid"])

    ssid = "WiFi not found"

    for line in scanoutput.split():
        line = line.decode("utf-8")
        if line[:5]  == "ESSID":
         ssid = line.split('"')[1]

    return str(ssid)


# Set the wifi ssid and password
# Hack: run these lines before
# sudo chmod a+r /etc/wpa_supplicant/wpa_supplicant.conf
# sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf
# def setWifi(ssid, pwd):

#     print("Setting wifi to", ssid, pwd)

#     os.popen("sudo chmod a+r /etc/wpa_supplicant/wpa_supplicant.conf")
#     os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

#     with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as conf:
#         lines = conf.readlines()

#     for i in range(len(lines)):
#        print(">>>>", lines[i])
#        if lines[i].find('ssid')!=-1:
#           lines[i] = '\tssid="' + ssid + '"\n'
#        elif lines[i].find('psk')!=-1:
#           lines[i] = '\tpsk="' + pwd + '"\n'

#     with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as conf:
#        conf.writelines(lines)

#     os.popen("sudo wpa_cli -i wlan0 reconfigure")

#     print(lines)

#https://maskaravivek.medium.com/python-script-to-configure-wifi-on-raspberry-pi-without-reboot-3af07368b3c2
def setWifi(ssid, password):
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
    
    #give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    
    #writing to file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
    
    print("Wifi config added. Refreshing configs")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")


# Get settins from a wifi.txt file on a USB drive
# First line in file is ssid
# Second line is password
def getSettings():
    mediaDir = "/media/pi/"
    #mediaDir = "/"

    # Find USB drives connected
    dirs = [f for f in os.listdir(mediaDir) if os.path.isdir(mediaDir+f)]
    #dirs = [f for f in os.listdir(mediaDir)]

    print("USB drives", dirs)

    if len(dirs)==0:
       return "No USB Drives Found"

    configFile = mediaDir + dirs[0] + "/wifi.txt"

    if not os.path.isfile(configFile):
       return "No wifi.txt config file found"
           
    # Read config file
    with open(configFile, "r") as conf:
        lines = conf.readlines()

    if len(lines)<2:
        return "Invalid wifi.txt config file"

    return (lines[0].strip(), lines[1].strip())