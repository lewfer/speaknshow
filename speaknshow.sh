DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Speaknshow started at ${DATE}" | systemd-cat -p info

echo "Speaknshow started at ${DATE}" > ~/voiceimage_startup.txt
#sleep 120

cd /home/pi/speaknshow
#python3 voiceimage.py & >> ~/voiceimage_startup.txt 2> ~/voiceimage_startup_err.txt

export XDG_RUNTIME_DIR="/run/user/1000"
python3 speaknshow.py &

