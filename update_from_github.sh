rm -r -f /home/pi/speaknshow-temp/* 2> ~/errors
rm -r -f /home/pi/speaknshow-temp/.* 2>> ~/errors
git clone https://github.com/lewfer/speaknshow.git /home/pi/speaknshow-temp -q
cp -r /home/pi/speaknshow-temp/* /home/pi/speaknshow/
rm -r -f /home/pi/speaknshow-temp/* 2>> ~/errors
rm -r -f /home/pi/speaknshow-temp/.* 2>> ~/errors
chmod +x /home/pi/speaknshow/*.sh

