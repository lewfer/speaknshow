DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Speaknshow started at ${DATE}" | systemd-cat -p info

echo "Speaknshow started at ${DATE}" > ~/voiceimage_startup.txt
#sleep 60

cd /home/pi/speaknshow
# The export line ensures the sound device works
export XDG_RUNTIME_DIR="/run/user/1000"
python3 speaknshow.py

