sudo apt update
sudo apt install -y python3-pip
pip3 install selenium==3.141.0
pip3 install pyvirtualdisplay
pip3 install 2captcha-python
sudo apt install -y unzip
sudo apt install -y xvfb
sudo apt install -y sqlite3
pip3 install sqlalchemy
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
wget -O t.py https://raw.githubusercontent.com/hbutt877/nust/master/t.py
wget -O job_t.sh https://raw.githubusercontent.com/hbutt877/nust/master/job_t.sh
wget -O login.py https://raw.githubusercontent.com/hbutt877/nust/master/login.py
wget -O job_l.sh https://raw.githubusercontent.com/hbutt877/nust/master/job_l.sh
wget -O captcha.py https://raw.githubusercontent.com/hbutt877/nust/master/captcha.py
rm chromedriver_linux64.zip
rm google-chrome-stable_current_amd64.deb
mkdir pics
chmod +x job_t.sh
chmod +x job_l.sh
